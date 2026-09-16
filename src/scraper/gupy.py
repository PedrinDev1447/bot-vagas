import httpx

from src.scraper.base import Scraper, Vaga

GUPY_JOBS_URL = "https://employability-portal.gupy.io/api/v1/jobs"
PAGE_SIZE = 100
MAX_PAGES_PER_PASS = 5  # teto de segurança para nao estourar o tempo do runner

SP_STATE_QUERY = "São Paulo"


def parse_gupy_job(raw: dict) -> Vaga:
    """Mapeia um item de `data[]` da API da Gupy para o modelo interno.

    Campos usados aqui sao exatamente os confirmados na spec (evidencia real
    de 2026-09-15/16) — nao inventar campo novo sem confirmar na fonte antes.
    """
    return Vaga(
        source="gupy",
        external_id=str(raw["id"]),
        title=raw["name"],
        company=raw["careerPageName"],
        city=raw["city"],
        state=raw["state"],
        workplace_type=raw["workplaceType"],
        url=raw["jobUrl"],
        published_at=raw.get("publishedDate"),
        application_deadline=raw.get("applicationDeadline"),
        description=raw["description"],
        source_seniority_hint=(
            "internship" if raw.get("type") == "vacancy_type_internship" else None
        ),
    )


class GupyScraper(Scraper):
    source = "gupy"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(timeout=20.0)

    def search(self, term: str) -> list[Vaga]:
        """Dois passes por termo (achado 2 da spec): a API devolve `city`/`state`
        vazios para vaga remota, entao filtrar por state no servidor excluiria
        toda vaga remota silenciosamente. Passe A pega SP presencial/hibrido;
        Passe B busca sem filtro de state e mantem so as remotas."""
        by_external_id: dict[str, Vaga] = {}

        for vaga in self._search_pass(term, state=SP_STATE_QUERY):
            by_external_id[vaga.external_id] = vaga

        for vaga in self._search_pass(term, state=None):
            if vaga.workplace_type == "remote":
                by_external_id[vaga.external_id] = vaga

        return list(by_external_id.values())

    def _search_pass(self, term: str, state: str | None) -> list[Vaga]:
        vagas: list[Vaga] = []
        offset = 0
        for _ in range(MAX_PAGES_PER_PASS):
            params: dict[str, str | int] = {
                "jobName": term,
                "limit": PAGE_SIZE,
                "offset": offset,
            }
            if state:
                params["state"] = state

            response = self._client.get(GUPY_JOBS_URL, params=params)
            response.raise_for_status()
            payload = response.json()

            vagas.extend(parse_gupy_job(raw) for raw in payload["data"])

            total = payload["pagination"]["total"]
            offset += PAGE_SIZE
            if offset >= total:
                break

        return vagas
