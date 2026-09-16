import argparse
import os
import sys
import time
from datetime import UTC, datetime

from dotenv import load_dotenv

from src.alerter.telegram import format_message, send_message
from src.exporter.markdown import append_ats_entry
from src.matcher.rules import (
    classify_seniority,
    is_blacklisted,
    is_it_title,
    is_vip,
    matched_stack_terms,
    passes_formacao_filter,
    passes_geo_filter,
    within_backfill_window,
)
from src.scraper.base import Vaga
from src.scraper.gupy import GupyScraper
from src.storage.db import connect, insert_vaga, mark_alerted

# Termos de busca cobrindo o espaco de senioridade da D4 (estagio/junior/trainee).
# config/search_terms.yaml fica pra quando houver mais de uma fonte (issue #2/#3).
SEARCH_TERMS = ["estagio", "estágio", "junior", "júnior", "trainee"]

DB_PATH = "vagas.db"
ATS_EXPORT_PATH = "vagas_ats.md"

# Defesa extra alem da janela de backfill de 24h (issue #1 ponto 6): mesmo com
# volume reduzido, um intervalo minimo entre envios reais evita estourar o
# limite de ~1 msg/s por chat da API do Telegram (429 + retry_after).
MIN_SECONDS_BETWEEN_SENDS = 1.0


def collect_candidates(scraper: GupyScraper) -> dict[str, Vaga]:
    """Busca todos os termos e funde por external_id — a mesma vaga pode
    aparecer sob mais de um termo de busca."""
    by_external_id: dict[str, Vaga] = {}
    for term in SEARCH_TERMS:
        for vaga in scraper.search(term):
            by_external_id[vaga.external_id] = vaga
    return by_external_id


def run(debug: bool) -> None:
    conn = connect(DB_PATH)
    reference_now = datetime.now(UTC)
    scraper = GupyScraper()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not debug and not (token and chat_id):
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID precisam estar setados fora do modo --debug."
        )

    candidates = collect_candidates(scraper)
    sent = 0

    for vaga in candidates.values():
        if is_blacklisted(vaga):
            continue
        if not is_it_title(vaga):
            continue
        if not passes_geo_filter(vaga):
            continue
        seniority = classify_seniority(vaga)
        if seniority is None:
            continue
        if not within_backfill_window(vaga, reference_now):
            continue
        if not passes_formacao_filter(vaga):
            continue
        terms = matched_stack_terms(vaga)
        vip = is_vip(vaga)
        if not terms and not vip:
            continue

        is_new = insert_vaga(conn, vaga, matched_terms=terms, seniority=seniority)
        if not is_new:
            continue

        text = format_message(vaga, terms, vip=vip)

        if debug:
            print(f"[DEBUG] enviaria:\n{text}\n")
        else:
            append_ats_entry(vaga, terms, seniority, vip, path=ATS_EXPORT_PATH)
            send_message(token, chat_id, text)
            mark_alerted(conn, vaga.source, vaga.external_id)
            time.sleep(MIN_SECONDS_BETWEEN_SENDS)

        sent += 1

    print(f"{sent} vaga(s) nova(s) processada(s).")


def main() -> None:
    # Terminal do Windows costuma abrir em cp1252; titulo/descricao tem acento.
    sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv()  # TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID vem de .env, nunca hardcoded
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    run(debug=args.debug)


if __name__ == "__main__":
    main()
