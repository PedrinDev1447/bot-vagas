import copy
import json
from pathlib import Path

import httpx
import pytest

from src.scraper.eureca import MAX_PAGES, EurecaScraper, _normalize, parse_eureca_opportunity

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "eureca_opportunities_response.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def fixture_record(opportunity_id: str) -> dict:
    return next(r for r in load_fixture()["items"] if r["id"] == opportunity_id)


def test_parse_eureca_opportunity_maps_hybrid_sp_fields():
    """Vaga real hibrida em SP, capturada em 2026-09-16 — stateAcronym "SP" deve
    virar o nome completo "São Paulo" pra bater com o filtro geografico do
    matcher (achado da spec: matcher compara contra nome completo, nao sigla)."""
    raw = fixture_record("01a091b8-3b35-7097-b331-6cfd80e3864e")  # Estagio Motiva
    vaga = parse_eureca_opportunity(raw)

    assert vaga.source == "eureca"
    assert vaga.external_id == "01a091b8-3b35-7097-b331-6cfd80e3864e"
    assert vaga.title == "Estágio em Gestão de Projetos de Engenharia | Vaga Afirmativa para PcD"
    assert vaga.company == "Motiva"
    assert vaga.city == "Jundiaí"
    assert vaga.state == "São Paulo"
    assert vaga.workplace_type == "hybrid"
    assert vaga.url == "https://app.eureca.me/vagas/01a091b8-3b35-7097-b331-6cfd80e3864e"
    assert vaga.application_deadline == "2027-01-01T02:59:00.000Z"
    assert vaga.source_seniority_hint == "internship"


def test_parse_eureca_opportunity_remote_workmodel_maps_to_remote():
    """workModel "remoto" deve virar workplace_type "remote" (vocabulario
    exigido por schema.sql e matcher/rules.py)."""
    raw = fixture_record("01a03eaf-7210-7b61-bf53-c69bcc8b6083")  # Curso MRS remoto
    vaga = parse_eureca_opportunity(raw)

    assert vaga.workplace_type == "remote"


def test_parse_eureca_opportunity_presencial_workmodel_maps_to_on_site():
    """workModel "presencial" deve virar workplace_type "on-site"."""
    raw = fixture_record("01a08cf9-3da6-7914-b448-251518d47749")  # Estagio Sabesp
    vaga = parse_eureca_opportunity(raw)

    assert vaga.workplace_type == "on-site"


def test_parse_eureca_opportunity_missing_city_state_becomes_empty_string():
    """Achado real: vaga presencial sem cityName/stateAcronym preenchidos
    (Estagio Sabesp) nao pode virar `None` no Vaga, que exige `str`."""
    raw = fixture_record("01a08cf9-3da6-7914-b448-251518d47749")
    vaga = parse_eureca_opportunity(raw)

    assert vaga.city == ""
    assert vaga.state == ""


def test_parse_eureca_opportunity_null_published_at_falls_back_to_created_at():
    """Confirmado pelo usuario: publishedAt vem null com frequencia — cai pra
    createdAt nesse caso."""
    raw = fixture_record("01a08cf9-3da6-7914-b448-251518d47749")
    assert raw["publishedAt"] is None

    vaga = parse_eureca_opportunity(raw)

    assert vaga.published_at == raw["createdAt"]


def test_parse_eureca_opportunity_present_published_at_is_used_as_is():
    """Todo registro capturado ate agora tem publishedAt null — mas o campo
    existe no schema confirmado e o docstring de parse_eureca_opportunity
    descreve o fallback como excecao ("com frequencia", nao sempre). Quando
    populado, published_at deve usar o valor de publishedAt, nao createdAt."""
    raw = copy.deepcopy(fixture_record("01a08cf9-3da6-7914-b448-251518d47749"))
    raw["publishedAt"] = "2026-09-11T12:00:00.000Z"

    vaga = parse_eureca_opportunity(raw)

    assert vaga.published_at == "2026-09-11T12:00:00.000Z"
    assert vaga.published_at != raw["createdAt"]


def test_parse_eureca_opportunity_internship_contract_type_sets_seniority_hint():
    raw = fixture_record("01a08cf9-3da6-7914-b448-251518d47749")  # internship
    vaga = parse_eureca_opportunity(raw)

    assert vaga.source_seniority_hint == "internship"


def test_parse_eureca_opportunity_non_internship_contract_type_has_no_hint():
    raw = fixture_record("01a03539-eb3c-74ca-ba68-72a89c4bd786")  # trainee
    vaga = parse_eureca_opportunity(raw)

    assert vaga.source_seniority_hint is None


def test_search_paginates_until_total_is_covered():
    """A API nao aceita filtro de busca (confirmado): search() deve varrer
    todas as paginas ate cobrir o `total` antes de filtrar no cliente."""
    all_records = load_fixture()["items"]
    page_1, page_2 = all_records[:5], all_records[5:]
    requested_pages = []

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params["page"])
        requested_pages.append(page)
        items = page_1 if page == 1 else page_2
        return httpx.Response(
            200,
            json={"items": items, "total": len(all_records), "page": page, "pageSize": 5},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    vagas = scraper.search("estagio")

    assert requested_pages == [1, 2]
    external_ids = {v.external_id for v in vagas}
    # todas as vagas cujo titulo/descricao normalizado (sem acento) contem
    # "estagio", MAIS as de contractTypeKey internship (bypass do filtro).
    expected = {
        r["id"]
        for r in all_records
        if r.get("contractTypeKey") == "internship"
        or "estagio" in _normalize(f"{r['name']}\n{r['description']}")
    }
    assert external_ids == expected
    assert external_ids  # nao pode ser vazio — regressao do filtro client-side


def test_search_term_not_found_returns_only_internship_bypass_records():
    """Termo que nao aparece em nenhum titulo/descricao nao zera o resultado:
    vagas com contractTypeKey "internship" contornam o filtro de termo
    (achado do red-team review, 2026-09-17) — sem isso, um estagio real cujo
    texto nao contem o termo buscado seria descartado silenciosamente."""
    all_records = load_fixture()["items"]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"items": all_records, "total": len(all_records), "page": 1, "pageSize": 8},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    vagas = scraper.search("desenvolvedor python senior blockchain")
    external_ids = {v.external_id for v in vagas}

    expected = {r["id"] for r in all_records if r.get("contractTypeKey") == "internship"}
    assert external_ids == expected
    assert len(expected) == 4  # SLC, Sabesp, Motiva, Comunidade de Talentos


def test_search_reuses_cached_items_across_calls():
    """search() e chamado uma vez por termo em main.py (5 termos) — sem
    cache por instancia, cada chamada re-buscaria todas as paginas da API
    (achado do performance review, 2026-09-17)."""
    all_records = load_fixture()["items"]
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        return httpx.Response(
            200,
            json={"items": all_records, "total": len(all_records), "page": 1, "pageSize": 8},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    scraper.search("estagio")
    scraper.search("trainee")
    scraper.search("junior")

    assert request_count == 1


def test_fetch_all_propagates_http_error_on_non_2xx_response():
    """Erro do servidor (fonte fora do ar) precisa propagar em vez de ser
    engolido — main.py decide o que fazer com a falha, o scraper nao deve
    mascarar como lista vazia."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "internal"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    with pytest.raises(httpx.HTTPStatusError):
        scraper.search("estagio")


def test_fetch_all_stops_at_max_pages_when_total_never_satisfied():
    """Teto de seguranca contra paginacao sem fim: se `total` nunca bater com
    o que foi acumulado (API instavel/paginacao quebrada), o loop precisa
    parar em MAX_PAGES em vez de rodar indefinidamente."""
    requested_pages = []

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params["page"])
        requested_pages.append(page)
        return httpx.Response(
            200,
            json={"items": [{"id": f"x{page}"}], "total": 10_000, "page": page, "pageSize": 8},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    items = scraper._fetch_all()

    assert len(requested_pages) == MAX_PAGES
    assert len(items) == MAX_PAGES


def test_normalize_handles_none_and_empty_string():
    """_normalize precisa aceitar None (campos opcionais do payload real, ex.
    cityName/stateAcronym) sem estourar — mesmo contrato do `or ""` usado em
    parse_eureca_opportunity."""
    assert _normalize(None) == ""
    assert _normalize("") == ""


def test_normalize_strips_accents_and_lowercases():
    """Base da busca client-side: precisa casar "Estágio" com "estagio" —
    sem essa normalizacao o filtro por termo perderia vaga real (ex. o
    proprio titulo "Estágio Sabesp 2027" do payload capturado)."""
    assert _normalize("Estágio") == "estagio"
    assert _normalize("  AÇÃO  ") == "acao"


def test_search_is_case_and_accent_insensitive_on_the_query_term():
    """O termo de busca passado pelo matcher pode vir com acento/maiuscula
    (ex. "Estágio"); search() precisa normalizar o termo igual normaliza o
    haystack, senao perde vaga por causa so de acentuacao na query."""
    all_records = load_fixture()["items"]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"items": all_records, "total": len(all_records), "page": 1, "pageSize": 8},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    accented_upper = {v.external_id for v in scraper.search("ESTÁGIO")}
    plain_lower = {v.external_id for v in scraper.search("estagio")}

    assert accented_upper == plain_lower
    assert accented_upper  # regressao: nao pode zerar por causa de acento/caixa


def test_fetch_all_stops_immediately_when_total_is_zero():
    """Resultado vazio (nenhuma vaga aberta no momento) e um estado real e
    valido da API — _fetch_all precisa parar na primeira pagina em vez de
    varrer ate MAX_PAGES, e search() precisa devolver lista vazia sem erro."""
    requested_pages = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_pages.append(int(request.url.params["page"]))
        return httpx.Response(200, json={"items": [], "total": 0, "page": 1, "pageSize": 8})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    scraper = EurecaScraper(client=client)

    assert scraper.search("estagio") == []
    assert requested_pages == [1]


def test_parse_eureca_opportunity_missing_work_model_key_becomes_empty_string():
    """workModel e lido via raw.get (defensivo) — se a chave nao vier no
    payload (nao so null, ausente mesmo), workplace_type precisa virar ""
    em vez de None, que quebraria o contrato `str` do Vaga."""
    raw = copy.deepcopy(fixture_record("01a091b8-3b35-7097-b331-6cfd80e3864e"))
    del raw["workModel"]

    vaga = parse_eureca_opportunity(raw)

    assert vaga.workplace_type == ""


def test_parse_eureca_opportunity_unrecognized_work_model_falls_back_to_raw_value():
    """workModel fora do vocabulario mapeado (remoto/presencial/hibrido) nao
    pode virar string vazia nem estourar — cai pro valor bruto da API, igual
    o fallback ja feito pra state_acronym desconhecido."""
    raw = copy.deepcopy(fixture_record("01a091b8-3b35-7097-b331-6cfd80e3864e"))
    raw["workModel"] = "flex"  # valor hipotetico fora do vocabulario conhecido

    vaga = parse_eureca_opportunity(raw)

    assert vaga.workplace_type == "flex"


def test_parse_eureca_opportunity_unrecognized_state_acronym_keeps_acronym():
    """stateAcronym fora do mapa (so "SP" esta mapeado hoje, unico estado que
    importa pro filtro geografico) precisa manter a sigla original em vez de
    virar string vazia — so acronimo ausente (None) deve virar ""."""
    raw = copy.deepcopy(fixture_record("01a091b8-3b35-7097-b331-6cfd80e3864e"))
    raw["stateAcronym"] = "RJ"
    raw["locations"]["states"] = []  # sem SP elegivel, senao prevaleceria sobre a sigla

    vaga = parse_eureca_opportunity(raw)

    assert vaga.state == "RJ"


def test_parse_eureca_opportunity_prefers_sao_paulo_capital_from_locations_over_city_name():
    """Achado do red-team review (2026-09-17): o `cityName` singular pode nao
    ser a capital mesmo quando Sao Paulo esta entre as cidades elegiveis da
    vaga em `locations.cities` — sem preferir a capital nesse caso, uma vaga
    valida pra SP falharia silenciosamente o filtro geografico do matcher
    (recall-first, D1 de specs/0001)."""
    raw = copy.deepcopy(fixture_record("01a03eaf-7210-7b61-bf53-c69bcc8b6083"))  # MRS Cubatao
    raw["locations"]["cities"] = ["Cubatão", "São Paulo", "Santos"]

    vaga = parse_eureca_opportunity(raw)

    assert vaga.city == "São Paulo"


def test_parse_eureca_opportunity_falls_back_to_city_name_when_sao_paulo_not_eligible():
    """Quando Sao Paulo capital nao esta entre as cidades elegiveis, usa o
    `cityName` singular normalmente (regressao: nao pode sempre virar SP)."""
    raw = fixture_record("01a03eaf-7210-7b61-bf53-c69bcc8b6083")  # MRS Cubatao — sem SP na lista

    vaga = parse_eureca_opportunity(raw)

    assert vaga.city == "Cubatão"


def test_parse_eureca_opportunity_prefers_sp_state_from_locations_when_acronym_unrecognized():
    """Mesmo raciocinio pro estado: "SP" em `locations.states` deve prevalecer
    sobre um `stateAcronym` singular ausente."""
    raw = copy.deepcopy(fixture_record("01a08cf9-3da6-7914-b448-251518d47749"))  # Sabesp
    raw["locations"]["states"] = ["SP"]

    vaga = parse_eureca_opportunity(raw)

    assert vaga.state == "São Paulo"


def test_parse_eureca_opportunity_state_locations_membership_is_case_insensitive():
    """Achado do adversarial review (2026-09-17): a checagem de "SP" em
    locations.states era case-sensitive, ao contrario de _resolve_city que ja
    normaliza — um "sp" minusculo vindo da API deixaria de bater."""
    raw = copy.deepcopy(fixture_record("01a08cf9-3da6-7914-b448-251518d47749"))  # Sabesp
    raw["locations"]["states"] = ["sp"]

    vaga = parse_eureca_opportunity(raw)

    assert vaga.state == "São Paulo"


def test_parse_eureca_opportunity_workmodel_lookup_is_case_insensitive():
    """Achado do adversarial review (2026-09-17): o lookup de workModel no
    dicionario WORK_MODEL_TO_WORKPLACE_TYPE nao normalizava a chave, ao
    contrario do resto do arquivo — um "REMOTO"/"Remoto" da API quebraria
    silenciosamente o bypass do filtro geografico em passes_geo_filter, que
    so aceita workplace_type == "remote" exato."""
    raw = copy.deepcopy(fixture_record("01a03eaf-7210-7b61-bf53-c69bcc8b6083"))  # MRS remoto
    raw["workModel"] = "REMOTO"

    vaga = parse_eureca_opportunity(raw)

    assert vaga.workplace_type == "remote"
