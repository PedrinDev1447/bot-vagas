import unicodedata

import httpx

from src.scraper.base import Scraper, Vaga

EURECA_OPPORTUNITIES_URL = "https://candidate-api.eureca.me/opportunities"
PAGE_SIZE = 8  # confirmado na captura real (2026-09-16)
MAX_PAGES = 25  # teto de seguranca contra paginacao sem fim

# So SP importa pro filtro geografico do bot (passes_geo_filter em matcher/rules.py
# compara contra o nome completo "sao paulo"); outros estados passam sem mapear.
STATE_ACRONYM_TO_NAME = {"SP": "São Paulo"}
SAO_PAULO_NORMALIZED = "sao paulo"  # espelha SP_NORMALIZED de matcher/rules.py

# schema.sql exige o vocabulario remote|hybrid|on-site; a Eureca devolve em
# portugues (confirmado no payload real de 2026-09-16). Chaves normalizadas
# (sem acento/caixa) porque o lookup em parse_eureca_opportunity normaliza
# work_model antes de comparar (achado do adversarial review, 2026-09-17:
# um "REMOTO"/"Remoto " nao normalizado quebraria o bypass do filtro
# geografico pra vaga remota em passes_geo_filter, ja que so bate exato).
WORK_MODEL_TO_WORKPLACE_TYPE = {
    "remoto": "remote",
    "presencial": "on-site",
    "hibrido": "hybrid",
}


def _normalize(text: str | None) -> str:
    """Lowercase, sem acento — mesma tecnica de matcher/rules.py, duplicada
    aqui pra nao criar dependencia scraper -> matcher (GupyScraper tambem
    nao depende do matcher)."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).lower().strip()


def _resolve_city(raw: dict) -> str:
    """Prefere São Paulo (capital) se estiver entre as cidades elegiveis da
    vaga (`locations.cities`), mesmo que o `cityName` singular escolhido pela
    API aponte outra cidade dentre as elegiveis — sem isso, uma vaga
    presencial valida pra capital falharia silenciosamente o filtro
    geografico do matcher (achado do red-team review, 2026-09-17;
    recall-first, D1 de specs/0001)."""
    cities = (raw.get("locations") or {}).get("cities") or []
    for city in cities:
        if _normalize(city) == SAO_PAULO_NORMALIZED:
            return city
    return raw.get("cityName") or ""


def _resolve_state_acronym(raw: dict) -> str | None:
    """Mesmo raciocinio de `_resolve_city` pro estado: se "SP" estiver entre
    os estados elegiveis da vaga (`locations.states`), prefere SP mesmo que
    `stateAcronym` singular esteja ausente ou aponte outro estado."""
    states = (raw.get("locations") or {}).get("states") or []
    if any(_normalize(state) == "sp" for state in states):
        return "SP"
    return raw.get("stateAcronym")


def parse_eureca_opportunity(raw: dict) -> Vaga:
    """Mapeia um item de `items[]` da API da Eureca (endpoint /opportunities)
    para o modelo interno. Campos confirmados via payload real capturado em
    2026-09-16 — nao inventar campo novo sem confirmar na fonte antes.

    `publishedAt` vem null com frequencia (caracteristica estrutural da API,
    confirmada pelo usuario) — cai pra `createdAt` nesse caso.
    """
    state_acronym = _resolve_state_acronym(raw)
    work_model = raw.get("workModel")

    return Vaga(
        source="eureca",
        external_id=raw["id"],
        title=raw["name"],
        company=raw["companyName"],
        city=_resolve_city(raw),
        state=STATE_ACRONYM_TO_NAME.get(state_acronym, state_acronym or ""),
        workplace_type=WORK_MODEL_TO_WORKPLACE_TYPE.get(_normalize(work_model), work_model or ""),
        url=f"https://app.eureca.me/vagas/{raw['id']}",
        published_at=raw.get("publishedAt") or raw.get("createdAt"),
        application_deadline=raw.get("endApplying"),
        description=raw["description"],
        source_seniority_hint=(
            "internship" if raw.get("contractTypeKey") == "internship" else None
        ),
    )


class EurecaScraper(Scraper):
    source = "eureca"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(timeout=20.0)
        self._items_cache: list[dict] | None = None

    def search(self, term: str) -> list[Vaga]:
        """O endpoint /opportunities nao aceita filtro de busca por palavra-
        chave (confirmado: a captura real foi so `?page=&pageSize=`, sem
        parametro de keyword/categoria) — busca todas as paginas e filtra no
        cliente por titulo/descricao, igual ao matcher faz downstream.

        Vagas com `contractTypeKey == "internship"` contornam o filtro de
        termo (mesmo tratamento do `source_seniority_hint` em
        `parse_eureca_opportunity`): sem isso, um estagio real cujo
        titulo/descricao nao contem o termo buscado seria descartado
        silenciosamente antes mesmo de chegar no `classify_seniority` do
        matcher (achado do red-team review, 2026-09-17)."""
        needle = _normalize(term)
        vagas = []
        for raw in self._fetch_all():
            is_internship = raw.get("contractTypeKey") == "internship"
            haystack = _normalize(f"{raw['name']}\n{raw['description']}")
            if is_internship or needle in haystack:
                vagas.append(parse_eureca_opportunity(raw))
        return vagas

    def _fetch_all(self) -> list[dict]:
        """Cacheado por instancia: `search()` e chamado uma vez por termo de
        busca em `main.py` (achado do performance review, 2026-09-17) — sem
        cache, isso re-buscaria todas as paginas por termo, multiplicando
        requisicoes ao endpoint da fonte sem necessidade, ja que a API nao
        filtra por termo no servidor."""
        if self._items_cache is not None:
            return self._items_cache

        items: list[dict] = []
        page = 1
        for _ in range(MAX_PAGES):
            response = self._client.get(
                EURECA_OPPORTUNITIES_URL,
                params={"page": page, "pageSize": PAGE_SIZE},
            )
            response.raise_for_status()
            payload = response.json()

            items.extend(payload["items"])

            if len(items) >= payload["total"]:
                break
            page += 1

        self._items_cache = items
        return items
