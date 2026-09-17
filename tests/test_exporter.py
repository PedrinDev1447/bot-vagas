from src.exporter.markdown import append_ats_entry
from src.scraper.base import Vaga

BASE_VAGA = Vaga(
    source="gupy",
    external_id="1",
    title="Desenvolvedor Java Junior",
    company="Acme",
    city="São Paulo",
    state="São Paulo",
    workplace_type="hybrid",
    url="https://example.com/job/1",
    published_at="2026-09-16T12:00:00.000Z",
    application_deadline=None,
    description="",
)


def test_append_creates_file_with_header_when_missing(tmp_path):
    path = str(tmp_path / "vagas_ats.md")

    append_ats_entry(BASE_VAGA, ["java", "spring boot"], "junior", vip=False, path=path)

    content = (tmp_path / "vagas_ats.md").read_text(encoding="utf-8")
    assert content.startswith("# Vagas ATS")
    assert "- [ ] **[Desenvolvedor Java Junior](https://example.com/job/1)**" in content
    assert "Acme" in content
    assert "hybrid" in content
    assert "junior" in content
    assert "java, spring boot" in content


def test_append_preserves_previous_entries(tmp_path):
    """Append-only (spec 0002): nao pode apagar checkboxes ja marcados pelo
    usuario em runs anteriores."""
    path = str(tmp_path / "vagas_ats.md")

    append_ats_entry(BASE_VAGA, ["java"], "junior", vip=False, path=path)
    (tmp_path / "vagas_ats.md").write_text(
        (tmp_path / "vagas_ats.md").read_text(encoding="utf-8").replace("- [ ]", "- [x]", 1),
        encoding="utf-8",
    )

    second_vaga = Vaga(
        source="gupy",
        external_id="2",
        title="Estagiario React",
        company="Beta",
        city="",
        state="",
        workplace_type="remote",
        url="https://example.com/job/2",
        published_at="2026-09-16T12:00:00.000Z",
        application_deadline=None,
        description="",
    )
    append_ats_entry(second_vaga, ["react"], "internship", vip=False, path=path)

    content = (tmp_path / "vagas_ats.md").read_text(encoding="utf-8")
    assert "- [x]" in content
    assert "Estagiario React" in content
    assert content.count("# Vagas ATS") == 1


def test_append_formats_vip_with_empty_terms(tmp_path):
    path = str(tmp_path / "vagas_ats.md")

    append_ats_entry(BASE_VAGA, [], "internship", vip=True, path=path)

    content = (tmp_path / "vagas_ats.md").read_text(encoding="utf-8")
    assert "sem termo de stack (via empresa VIP)" in content
    assert "⭐VIP" in content


def test_append_no_vip_tag_when_not_vip(tmp_path):
    path = str(tmp_path / "vagas_ats.md")

    append_ats_entry(BASE_VAGA, ["java"], "junior", vip=False, path=path)

    content = (tmp_path / "vagas_ats.md").read_text(encoding="utf-8")
    assert "⭐VIP" not in content
