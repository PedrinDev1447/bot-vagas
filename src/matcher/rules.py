import re
import unicodedata
from datetime import datetime, timedelta

from src.scraper.base import Vaga

# Perfil de referencia (CLAUDE.md): Java, Spring Boot, React, TypeScript, AWS.
# Issue #1: lista fixa, sem pesos — score ponderado fica pra issue #Z.
MINHA_STACK = ["java", "spring boot", "react", "typescript", "aws"]

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


def within_backfill_window(vaga: Vaga, reference_now: datetime, window_hours: int = 24) -> bool:
    """Issue #1 ponto 6: primeiro run so considera vagas publicadas dentro da
    janela (default 24h), pra nao estourar o limite de ~1 msg/s por chat da
    API do Telegram num backfill de banco vazio."""
    if not vaga.published_at:
        return False
    published = datetime.fromisoformat(vaga.published_at.replace("Z", "+00:00"))
    return reference_now - published <= timedelta(hours=window_hours)
