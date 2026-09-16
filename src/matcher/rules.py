import re
import unicodedata
from datetime import datetime, timedelta

from src.scraper.base import Vaga

# Perfil de referencia (CLAUDE.md): Java, Spring Boot, React, TypeScript, AWS.
# Issue #1: lista fixa, sem pesos — score ponderado fica pra issue #Z.
MINHA_STACK = ["java", "spring boot", "react", "typescript", "aws"]

# Empresas que sempre alertam, mesmo sem termo de MINHA_STACK no texto (bypassa
# is_stack_match — spec 0002). Sem YAML ainda, mesmo estilo enxuto de MINHA_STACK.
VIP_COMPANIES = [
    "itau",
    "itaú",
    "nubank",
    "mercado livre",
    "ifood",
    "stone",
    "xp",
    "inter",
    "quintoandar",
    "ambev tech",
    "aws",
    "microsoft",
    "google",
]

# Empresas que nunca alertam, independente de match de stack ou VIP.
# Vazia por padrao — estrutura pronta pra adicoes futuras.
BLACKLIST_COMPANIES: list[str] = []

# Minha previsao de formatura (spec 0002). So o ano entra na comparacao.
MINHA_FORMACAO_ANO = 2027

# Janela de caracteres apos a keyword de formacao onde procuramos um ano —
# grande o suficiente pra cobrir frases como "conclusao... entre X e Y".
FORMACAO_WINDOW_CHARS = 100
FORMACAO_KEYWORD_PATTERN = re.compile(r"formaca|formatura|conclu|formand")
FORMACAO_YEAR_PATTERN = re.compile(r"\b(20[2-3]\d)\b")

SP_NORMALIZED = "sao paulo"

# D4: a positiva vence a de exclusao quando ambas batem (ex.: "Junior/Pleno"
# ainda e vaga de entrada valida) — por isso so a positiva decide o resultado.
# Um titulo so-de-exclusao (ex.: "Desenvolvedor Senior") ja fica de fora por
# nao bater a positiva; nao ha caso em que a exclusao muda esse resultado.
# Ordem importa: primeiro padrao que bater define o rotulo salvo no banco.
SENIORITY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("internship", re.compile(r"estag|internship|intern")),
    ("trainee", re.compile(r"trainee")),
    ("junior", re.compile(r"junior|\bjr\b")),
]


def normalize(text: str | None) -> str:
    """Lowercase, sem acento, espacos nas pontas — base de comparacao pro
    filtro geografico (D3) e pro regex de senioridade (D4)."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return without_accents.lower().strip()


def passes_geo_filter(vaga: Vaga) -> bool:
    """D3: SP capital (presencial/hibrido) + remoto Brasil. Vaga remota vem com
    city/state vazios na Gupy (achado 2 da spec), entao o ramo remoto nao
    depende desses campos."""
    if vaga.workplace_type == "remote":
        return True
    return normalize(vaga.city) == SP_NORMALIZED and normalize(vaga.state) == SP_NORMALIZED


def classify_seniority(vaga: Vaga) -> str | None:
    """D4: campo `type` da Gupy decide estagio direto; caso contrario, regex
    positiva no titulo (estagio/trainee/junior). None = fora do perfil de
    entrada (senior, pleno, ou nenhum termo de entrada no titulo)."""
    if vaga.source_seniority_hint == "internship":
        return "internship"
    title = normalize(vaga.title)
    for label, pattern in SENIORITY_PATTERNS:
        if pattern.search(title):
            return label
    return None


def matched_stack_terms(vaga: Vaga) -> list[str]:
    """Matching simples da issue #1: quais termos de MINHA_STACK aparecem em
    titulo + descricao. Sem peso, sem threshold — score ponderado e a #Z."""
    haystack = normalize(f"{vaga.title}\n{vaga.description}")
    return [term for term in MINHA_STACK if normalize(term) in haystack]


def is_stack_match(vaga: Vaga) -> bool:
    return len(matched_stack_terms(vaga)) >= 1


def _company_haystack(vaga: Vaga) -> str:
    """company (careerPageName) + title + primeiros 500 chars da description,
    normalizados — mitigacao de slogan de carreira estilizado (ex.: Gupy
    #SANGUELARANJA) na deteccao de VIP/blacklist (spec 0002)."""
    return normalize(f"{vaga.company}\n{vaga.title}\n{vaga.description[:500]}")


def _matches_company_list(vaga: Vaga, companies: list[str]) -> bool:
    haystack = _company_haystack(vaga)
    return any(normalize(company) in haystack for company in companies)


def is_vip(vaga: Vaga) -> bool:
    return _matches_company_list(vaga, VIP_COMPANIES)


def is_blacklisted(vaga: Vaga) -> bool:
    return _matches_company_list(vaga, BLACKLIST_COMPANIES)


def passes_formacao_filter(vaga: Vaga) -> bool:
    """Conservador (spec 0002): so rejeita se a description citar
    formatura/conclusao limitada a um ano estritamente anterior a
    MINHA_FORMACAO_ANO. Sem mencao ou ambiguo -> aceita (recall-first, D1 da
    spec 0001) — o erro sempre pende pra aceitar, nunca pra descartar."""
    text = normalize(vaga.description)
    years_found = [
        int(year)
        for match in FORMACAO_KEYWORD_PATTERN.finditer(text)
        for year in FORMACAO_YEAR_PATTERN.findall(
            text[match.end() : match.end() + FORMACAO_WINDOW_CHARS]
        )
    ]
    if not years_found:
        return True
    return max(years_found) >= MINHA_FORMACAO_ANO


def within_backfill_window(vaga: Vaga, reference_now: datetime, window_hours: int = 24) -> bool:
    """Issue #1 ponto 6: primeiro run so considera vagas publicadas dentro da
    janela (default 24h), pra nao estourar o limite de ~1 msg/s por chat da
    API do Telegram num backfill de banco vazio."""
    if not vaga.published_at:
        return False
    published = datetime.fromisoformat(vaga.published_at.replace("Z", "+00:00"))
    return reference_now - published <= timedelta(hours=window_hours)
