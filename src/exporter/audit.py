from datetime import datetime
from pathlib import Path

from src.scraper.base import Vaga

AUDIT_LOG_PATH = "auditoria_rejeitadas.log"

REASON_BLACKLIST = "Empresa na blacklist"
REASON_NOT_IT_TITLE = "Cargo fora de TI"
REASON_GEO = "Fora da área geográfica (SP capital ou remoto Brasil)"
REASON_SENIORITY = "Senioridade fora do perfil (não é estágio/júnior/trainee)"
REASON_FORMACAO = "Formatura anterior ao ano-alvo"
REASON_STACK = "Sem match de stack (nem Core nem 2+ Adjacent)"


def log_rejection(vaga: Vaga, reason: str, now: datetime, path: str = AUDIT_LOG_PATH) -> None:
    """Append-only (mesmo padrao do ATS export, spec 0002) — nunca reescreve
    o arquivo. `now` e obrigatorio (sem leitura de relogio interna) pra ficar
    testavel como within_backfill_window."""
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    line = f"[{timestamp}] Rejeitada: {vaga.title} - {vaga.company} | Motivo: {reason}\n"
    with Path(path).open("a", encoding="utf-8") as f:
        f.write(line)
