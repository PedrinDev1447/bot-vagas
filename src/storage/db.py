import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from src.scraper.base import Vaga

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return conn


def insert_vaga(
    conn: sqlite3.Connection, vaga: Vaga, matched_terms: list[str], seniority: str
) -> bool:
    """Insere a vaga se for nova. Retorna True se inseriu, False se já existia
    (mesma source + external_id — regra de dedupe da issue #1)."""
    cursor = conn.execute(
        """
        INSERT INTO vagas (
            source, external_id, title, company, city, state, workplace_type,
            url, published_at, application_deadline, description, seniority,
            matched_terms, first_seen_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source, external_id) DO NOTHING
        """,
        (
            vaga.source,
            vaga.external_id,
            vaga.title,
            vaga.company,
            vaga.city,
            vaga.state,
            vaga.workplace_type,
            vaga.url,
            vaga.published_at,
            vaga.application_deadline,
            vaga.description,
            seniority,
            json.dumps(matched_terms, ensure_ascii=False),
            datetime.now(UTC).isoformat(),
        ),
    )
    conn.commit()
    return cursor.rowcount > 0


def mark_alerted(conn: sqlite3.Connection, source: str, external_id: str) -> None:
    conn.execute(
        "UPDATE vagas SET alerted_at = ? WHERE source = ? AND external_id = ?",
        (datetime.now(UTC).isoformat(), source, external_id),
    )
    conn.commit()
