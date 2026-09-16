import json
from dataclasses import replace

from src.scraper.base import Vaga
from src.storage.db import connect, insert_vaga, mark_alerted


def make_vaga(external_id: str = "111") -> Vaga:
    return Vaga(
        source="gupy",
        external_id=external_id,
        title="Desenvolvedor Java Junior",
        company="Acme",
        city="São Paulo",
        state="São Paulo",
        workplace_type="hybrid",
        url="https://example.com/job/111",
        published_at="2026-09-16T12:00:00.000Z",
        application_deadline="2026-10-01",
        description="Java e Spring Boot",
    )


def test_insert_new_vaga_returns_true(tmp_path):
    conn = connect(str(tmp_path / "vagas.db"))
    inserted = insert_vaga(
        conn, make_vaga(), matched_terms=["java", "spring boot"], seniority="junior"
    )
    assert inserted is True

    row = conn.execute("SELECT * FROM vagas WHERE external_id = ?", ("111",)).fetchone()
    assert row["source"] == "gupy"
    assert row["title"] == "Desenvolvedor Java Junior"
    assert json.loads(row["matched_terms"]) == ["java", "spring boot"]
    assert row["alerted_at"] is None


def test_duplicate_external_id_does_not_reinsert(tmp_path):
    """Regra de dedupe da issue #1: UNIQUE(source, external_id) apenas."""
    conn = connect(str(tmp_path / "vagas.db"))
    first = insert_vaga(conn, make_vaga(), matched_terms=["java"], seniority="junior")
    second = insert_vaga(conn, make_vaga(), matched_terms=["java"], seniority="junior")

    assert first is True
    assert second is False
    count = conn.execute("SELECT COUNT(*) AS n FROM vagas WHERE external_id = '111'").fetchone()[
        "n"
    ]
    assert count == 1


def test_same_external_id_different_source_is_not_a_duplicate(tmp_path):
    """Issue #1 nao tem hash canonico ainda (issue #X) — dedupe e so por
    (source, external_id), entao a mesma id vinda de outra fonte entra."""
    conn = connect(str(tmp_path / "vagas.db"))
    gupy_vaga = make_vaga(external_id="111")
    other_vaga = replace(gupy_vaga, source="greenhouse")

    first = insert_vaga(conn, gupy_vaga, matched_terms=["java"], seniority="junior")
    second = insert_vaga(conn, other_vaga, matched_terms=["java"], seniority="junior")

    assert first is True
    assert second is True


def test_mark_alerted_sets_timestamp(tmp_path):
    conn = connect(str(tmp_path / "vagas.db"))
    insert_vaga(conn, make_vaga(), matched_terms=["java"], seniority="junior")

    mark_alerted(conn, "gupy", "111")

    row = conn.execute("SELECT alerted_at FROM vagas WHERE external_id = '111'").fetchone()
    assert row["alerted_at"] is not None
