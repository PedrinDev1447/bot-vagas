from dataclasses import replace
from datetime import UTC, datetime

from src.matcher import rules as rules_module
from src.matcher.rules import (
    classify_seniority,
    is_blacklisted,
    is_vip,
    matched_stack_terms,
    passes_formacao_filter,
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


# --- VIP / blacklist de empresas (spec 0002) ---


def test_is_vip_matches_company_field_case_and_accent_insensitive():
    vaga = replace(BASE_VAGA, company="Nubank")
    assert is_vip(vaga) is True


def test_is_vip_matches_via_title_when_company_is_stylized():
    """Mitigacao de slogan de carreira estilizado (ex.: Gupy #SANGUELARANJA):
    o termo VIP pode bater no titulo mesmo quando company nao ajuda."""
    vaga = replace(BASE_VAGA, company="#SANGUELARANJA", title="Estagiario Itau de Tecnologia")
    assert is_vip(vaga) is True


def test_is_vip_matches_via_description_first_500_chars():
    vaga = replace(
        BASE_VAGA, company="Globalweb", title="Estagio", description="Vem trabalhar na Stone!"
    )
    assert is_vip(vaga) is True


def test_is_vip_false_when_no_match():
    vaga = replace(BASE_VAGA, company="Acme")
    assert is_vip(vaga) is False


def test_is_blacklisted_true_when_company_in_list(monkeypatch):
    monkeypatch.setattr(rules_module, "BLACKLIST_COMPANIES", ["acme"])
    vaga = replace(BASE_VAGA, company="Acme")
    assert is_blacklisted(vaga) is True


def test_is_blacklisted_false_by_default():
    """BLACKLIST_COMPANIES comeca vazia (spec 0002) — nenhuma empresa bloqueada."""
    vaga = replace(BASE_VAGA, company="Qualquer Empresa")
    assert is_blacklisted(vaga) is False


# --- filtro de elegibilidade por formacao (spec 0002) ---


def test_formacao_accepts_range_including_target_year():
    vaga = replace(
        BASE_VAGA,
        description="Previsão de conclusão do curso: entre Dezembro/2026 e Dezembro/2027.",
    )
    assert passes_formacao_filter(vaga) is True


def test_formacao_accepts_from_target_year_onward():
    vaga = replace(
        BASE_VAGA,
        description=(
            "Formação superior em andamento com previsão de formatura a partir de 12/2027."
        ),
    )
    assert passes_formacao_filter(vaga) is True


def test_formacao_accepts_range_phrasing_without_month():
    vaga = replace(
        BASE_VAGA,
        description=(
            "Disponibilidade para estagiar por pelo menos 1 ano (conclusão entre 2026 e 2027)."
        ),
    )
    assert passes_formacao_filter(vaga) is True


def test_formacao_rejects_deadline_before_target_year():
    vaga = replace(BASE_VAGA, description="Buscamos estudantes com formatura até dez/2026.")
    assert passes_formacao_filter(vaga) is False


def test_formacao_rejects_single_year_before_target():
    vaga = replace(BASE_VAGA, description="Requisito: conclusão em 2025.")
    assert passes_formacao_filter(vaga) is False


def test_formacao_accepts_when_no_mention():
    vaga = replace(BASE_VAGA, description="Java, Spring Boot e vontade de aprender.")
    assert passes_formacao_filter(vaga) is True
