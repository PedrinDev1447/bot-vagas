from dataclasses import replace
from datetime import UTC, datetime

from src.matcher.rules import (
    classify_seniority,
    matched_stack_terms,
    passes_geo_filter,
    within_backfill_window,
)
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


# --- filtro geografico (D3) ---


def test_geo_filter_accepts_sp_capital_hybrid():
    assert passes_geo_filter(BASE_VAGA) is True


def test_geo_filter_accepts_remote_with_empty_city_state():
    """Regressao do achado 2: vaga remota tem city/state vazios e ainda assim
    deve ser aceita."""
    vaga = replace(BASE_VAGA, workplace_type="remote", city="", state="")
    assert passes_geo_filter(vaga) is True


def test_geo_filter_rejects_other_state_hybrid():
    vaga = replace(BASE_VAGA, city="Juiz de Fora", state="Minas Gerais", workplace_type="on-site")
    assert passes_geo_filter(vaga) is False


# --- senioridade (D4) ---


def test_seniority_uses_source_hint_when_present():
    vaga = replace(BASE_VAGA, title="Qualquer coisa", source_seniority_hint="internship")
    assert classify_seniority(vaga) == "internship"


def test_seniority_positive_regex_junior():
    vaga = replace(BASE_VAGA, title="Desenvolvedor(a) Júnior", source_seniority_hint=None)
    assert classify_seniority(vaga) == "junior"


def test_seniority_positive_regex_trainee():
    vaga = replace(BASE_VAGA, title="Programa de Trainee 2027", source_seniority_hint=None)
    assert classify_seniority(vaga) == "trainee"


def test_seniority_exclusion_only_title_is_rejected():
    vaga = replace(BASE_VAGA, title="Desenvolvedor Sênior Java", source_seniority_hint=None)
    assert classify_seniority(vaga) is None


def test_seniority_mixed_title_positive_wins():
    """D4: titulo tipo 'Junior/Pleno' ainda e vaga de entrada valida."""
    vaga = replace(BASE_VAGA, title="Desenvolvedor Júnior/Pleno", source_seniority_hint=None)
    assert classify_seniority(vaga) == "junior"


def test_seniority_no_match_is_rejected():
    vaga = replace(BASE_VAGA, title="Recepcionista", source_seniority_hint=None)
    assert classify_seniority(vaga) is None


# --- matching de stack (issue #1: contagem simples, sem peso) ---


def test_matching_counts_multiple_stack_terms():
    vaga = replace(
        BASE_VAGA,
        title="Desenvolvedor Java Junior",
        description="Java, Spring Boot, React e AWS. TypeScript e um diferencial.",
    )
    terms = matched_stack_terms(vaga)
    assert set(terms) == {"java", "spring boot", "react", "typescript", "aws"}


def test_matching_single_term_still_counts():
    vaga = replace(BASE_VAGA, title="Estagio", description="Sera um diferencial saber AWS.")
    assert matched_stack_terms(vaga) == ["aws"]


def test_matching_no_terms_returns_empty():
    vaga = replace(BASE_VAGA, title="Estagio Administrativo", description="Excel e organizacao.")
    assert matched_stack_terms(vaga) == []


# --- backfill do primeiro run (issue #1, ponto 6) ---


def test_backfill_accepts_job_published_within_24h():
    reference_now = datetime(2026, 9, 16, 20, 0, 0, tzinfo=UTC)
    vaga = replace(BASE_VAGA, published_at="2026-09-16T12:00:00.000Z")  # 8h atras
    assert within_backfill_window(vaga, reference_now) is True


def test_backfill_rejects_job_older_than_24h():
    reference_now = datetime(2026, 9, 16, 20, 0, 0, tzinfo=UTC)
    vaga = replace(BASE_VAGA, published_at="2026-08-05T15:15:04.818Z")  # semanas atras
    assert within_backfill_window(vaga, reference_now) is False


def test_backfill_rejects_missing_published_date():
    reference_now = datetime(2026, 9, 16, 20, 0, 0, tzinfo=UTC)
    vaga = replace(BASE_VAGA, published_at=None)
    assert within_backfill_window(vaga, reference_now) is False
