from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

from src.exporter.audit import REASON_STACK, log_rejection
from src.scraper.base import Vaga

BASE_VAGA = Vaga(
    source="gupy",
    external_id="1",
    title="Desenvolvedor Junior",
    company="Acme",
    city="São Paulo",
    state="São Paulo",
    workplace_type="hybrid",
    url="https://example.com/1",
    published_at="2026-09-16T12:00:00.000Z",
    application_deadline=None,
    description="",
)

NOW = datetime(2026, 9, 16, 20, 5, 0, tzinfo=UTC)


def test_log_rejection_appends_line_in_expected_format(tmp_path):
    path = str(tmp_path / "auditoria_rejeitadas.log")

    log_rejection(BASE_VAGA, REASON_STACK, NOW, path=path)

    content = Path(path).read_text(encoding="utf-8")
    assert content == (
        f"[2026-09-16 20:05] Rejeitada: Desenvolvedor Junior - Acme | Motivo: {REASON_STACK}\n"
    )


def test_log_rejection_appends_without_truncating_existing_content(tmp_path):
    path = str(tmp_path / "auditoria_rejeitadas.log")
    outra_vaga = replace(BASE_VAGA, title="Outra Vaga", company="Beta")

    log_rejection(BASE_VAGA, REASON_STACK, NOW, path=path)
    log_rejection(outra_vaga, REASON_STACK, NOW, path=path)

    lines = Path(path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert "Desenvolvedor Junior - Acme" in lines[0]
    assert "Outra Vaga - Beta" in lines[1]
