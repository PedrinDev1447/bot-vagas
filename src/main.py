import argparse
import os
import sys
from datetime import UTC, datetime

from src.alerter.telegram import send_message
from src.matcher.rules import (
    classify_seniority,
    is_stack_match,
    matched_stack_terms,
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
        if not passes_geo_filter(vaga):
            continue
        seniority = classify_seniority(vaga)
        if seniority is None:
            continue
        if not within_backfill_window(vaga, reference_now):
            continue
        terms = matched_stack_terms(vaga)
        if not is_stack_match(vaga):
            continue

        is_new = insert_vaga(conn, vaga, matched_terms=terms, seniority=seniority)
        if not is_new:
            continue

        text = (
            f"{vaga.title} — {vaga.company}\n"
            f"{vaga.workplace_type} | {vaga.city or 'remoto'}\n"
            f"Termos: {', '.join(terms)}\n"
            f"{vaga.url}"
        )

        if debug:
            print(f"[DEBUG] enviaria:\n{text}\n")
        else:
            send_message(token, chat_id, text)
            mark_alerted(conn, vaga.source, vaga.external_id)

        sent += 1

    print(f"{sent} vaga(s) nova(s) processada(s).")


def main() -> None:
    # Terminal do Windows costuma abrir em cp1252; titulo/descricao tem acento.
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    run(debug=args.debug)


if __name__ == "__main__":
    main()
