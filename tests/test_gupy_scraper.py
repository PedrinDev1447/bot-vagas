import json
from pathlib import Path

import httpx

from src.scraper.gupy import GupyScraper, parse_gupy_job

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "gupy_search_response.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def fixture_record(job_id: int) -> dict:
    return next(r for r in load_fixture()["data"] if r["id"] == job_id)


def test_parse_gupy_job_maps_onsite_hybrid_fields():
    """Vaga real SP/hibrido, capturada em 2026-09-16 — campos exatamente como
    a API devolveu, sem inventar nada."""
    raw = fixture_record(12507135)
    vaga = parse_gupy_job(raw)

    assert vaga.source == "gupy"
    assert vaga.external_id == "12507135"
    assert vaga.title == "Estágio | Trabalhista "
    assert vaga.company == "Pellegrina & Monteiro Advogados"
    assert vaga.city == "São Paulo"
    assert vaga.state == "São Paulo"
    assert vaga.workplace_type == "hybrid"
    assert vaga.url.startswith("https://pellegrinaemonteiro.gupy.io/job/")
    assert vaga.published_at == "2026-09-16T19:39:04.153Z"
    assert vaga.application_deadline == "2026-10-26"
    assert vaga.source_seniority_hint == "internship"


def test_parse_gupy_job_remote_has_empty_city_state():
    """Achado 2 da spec: vaga remota vem com city/state vazios na Gupy."""
    raw = fixture_record(12484628)
    vaga = parse_gupy_job(raw)

    assert vaga.workplace_type == "remote"
    assert vaga.city == ""
    assert vaga.state == ""
    assert vaga.source_seniority_hint == "internship"


def test_parse_gupy_job_effective_type_has_no_internship_hint():
    """type == vacancy_type_effective (nao-estagio) nao deve virar hint de
    estagio — senioridade sai da regex de titulo pro matcher decidir."""
    raw = fixture_record(11952340)
    vaga = parse_gupy_job(raw)

    assert vaga.source_seniority_hint is None
    assert vaga.title == "Desenvolvedor Java Junior"


def test_search_two_pass_merges_sp_and_remote_without_duplicating():
    """Passe A (state=SP) pega presencial/hibrido de SP; Passe B (sem state)
    mantem so as remotas. A vaga de MG (nem SP nem remota) nao deve aparecer
    em nenhum dos dois passes — regressao do achado 2."""
    sp_record = fixture_record(12507135)  # SP hibrido
    java_sp_record = fixture_record(11952340)  # SP hibrido
    remote_record = fixture_record(12484628)  # remoto, city/state vazios
    mg_record = fixture_record(12478431)  # MG on-site — nao deve sobreviver

    def handler(request: httpx.Request) -> httpx.Response:
        params = request.url.params
        if params.get("state"):
            data = [sp_record, java_sp_record]
        else:
            data = [sp_record, remote_record, mg_record, java_sp_record]
        return httpx.Response(
            200, json={"data": data, "pagination": {"total": len(data), "limit": 100, "offset": 0}}
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = GupyScraper(client=client)

    vagas = scraper.search("estagio")
    external_ids = {v.external_id for v in vagas}

    assert external_ids == {"12507135", "11952340", "12484628"}
    assert "12478431" not in external_ids
