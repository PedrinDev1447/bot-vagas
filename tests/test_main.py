from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

import src.main as main_module
from src.scraper.base import Vaga
from src.storage.db import connect

NOW = datetime(2026, 9, 16, 20, 0, 0, tzinfo=UTC)


def make_vaga(**overrides) -> Vaga:
    base = Vaga(
        source="gupy",
        external_id="1",
        title="Desenvolvedor Java Junior",
        company="Acme",
        city="São Paulo",
        state="São Paulo",
        workplace_type="hybrid",
        url="https://example.com/job/1",
        published_at="2026-09-16T12:00:00.000Z",  # 8h antes de NOW — dentro do backfill
        application_deadline=None,
        description="Java e Spring Boot",
    )
    return replace(base, **overrides)


def setup_run(monkeypatch, tmp_path, vagas, debug=False, with_token=True):
    db_path = str(tmp_path / "vagas.db")
    ats_path = str(tmp_path / "vagas_ats.md")
    monkeypatch.setattr(main_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "ATS_EXPORT_PATH", ats_path)
    monkeypatch.setattr(main_module.GupyScraper, "search", lambda self, term: list(vagas))
    monkeypatch.setattr(main_module.time, "sleep", lambda s: None)
    monkeypatch.setattr(
        main_module, "datetime", type("_FixedDatetime", (), {"now": staticmethod(lambda tz: NOW)})
    )
    if with_token:
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "123")
    else:
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    sent_calls = []
    monkeypatch.setattr(
        main_module,
        "send_message",
        lambda token, chat_id, text: sent_calls.append((token, chat_id, text)),
    )
    return db_path, sent_calls, ats_path


def test_run_sends_new_matching_vaga_and_marks_alerted(monkeypatch, tmp_path):
    db_path, sent_calls, ats_path = setup_run(monkeypatch, tmp_path, [make_vaga()])

    main_module.run(debug=False)

    assert len(sent_calls) == 1
    token, chat_id, text = sent_calls[0]
    assert (token, chat_id) == ("tok", "123")
    assert "Desenvolvedor Java Junior" in text

    conn = connect(db_path)
    row = conn.execute("SELECT alerted_at FROM vagas WHERE external_id = ?", ("1",)).fetchone()
    assert row["alerted_at"] is not None

    assert "Desenvolvedor Java Junior" in Path(ats_path).read_text(encoding="utf-8")


def test_run_twice_does_not_resend_same_vaga(monkeypatch, tmp_path):
    """Idempotencia: dedupe por (source, external_id) impede reenvio."""
    db_path, sent_calls, _ = setup_run(monkeypatch, tmp_path, [make_vaga()])

    main_module.run(debug=False)
    main_module.run(debug=False)

    assert len(sent_calls) == 1


def test_run_debug_mode_does_not_call_telegram(monkeypatch, tmp_path, capsys):
    _, sent_calls, ats_path = setup_run(monkeypatch, tmp_path, [make_vaga()], with_token=False)

    main_module.run(debug=True)

    assert sent_calls == []
    out = capsys.readouterr().out
    assert "Desenvolvedor Java Junior" in out
    assert not Path(ats_path).exists()


def test_run_without_token_outside_debug_raises(monkeypatch, tmp_path):
    setup_run(monkeypatch, tmp_path, [], with_token=False)

    with pytest.raises(SystemExit):
        main_module.run(debug=False)


def test_run_skips_vaga_outside_geo_filter(monkeypatch, tmp_path):
    vaga = make_vaga(city="Juiz de Fora", state="Minas Gerais", workplace_type="on-site")
    _, sent_calls, _ = setup_run(monkeypatch, tmp_path, [vaga])

    main_module.run(debug=False)

    assert sent_calls == []


def test_run_skips_vaga_outside_backfill_window(monkeypatch, tmp_path):
    vaga = make_vaga(published_at="2026-08-05T15:15:04.818Z")  # semanas antes de NOW
    _, sent_calls, _ = setup_run(monkeypatch, tmp_path, [vaga])

    main_module.run(debug=False)

    assert sent_calls == []


def test_run_skips_blacklisted_company_even_with_stack_match(monkeypatch, tmp_path):
    monkeypatch.setattr(main_module, "is_blacklisted", lambda vaga: True)
    _, sent_calls, ats_path = setup_run(monkeypatch, tmp_path, [make_vaga()])

    main_module.run(debug=False)

    assert sent_calls == []
    assert not Path(ats_path).exists()


def test_run_alerts_vip_company_without_stack_match(monkeypatch, tmp_path):
    """VIP bypassa so matched_stack_terms — o titulo ainda precisa ser de TI
    (fix spec 0003)."""
    vaga = make_vaga(
        company="Nubank",
        title="Estágio em Tecnologia",
        description="Vaga de estagio, sem termo de stack especifico.",
    )
    _, sent_calls, ats_path = setup_run(monkeypatch, tmp_path, [vaga])

    main_module.run(debug=False)

    assert len(sent_calls) == 1
    assert "VIP" in sent_calls[0][2]
    assert "sem termo de stack" in Path(ats_path).read_text(encoding="utf-8")


def test_run_rejects_vip_company_with_non_it_title(monkeypatch, tmp_path):
    """Fix spec 0003: empresa VIP tambem contrata fora de TI (RH, juridico) —
    VIP nunca bypassa a exigencia de titulo de TI."""
    vaga = make_vaga(company="Itaú", title="Estágio | Trabalhista")
    _, sent_calls, ats_path = setup_run(monkeypatch, tmp_path, [vaga])

    main_module.run(debug=False)

    assert sent_calls == []
    assert not Path(ats_path).exists()


def test_run_rejects_non_vip_company_matching_via_substring_only(monkeypatch, tmp_path):
    """Fix spec 0003: "inter"/"xp" nao podem bater como substring dentro de
    "internship"/"experiencia". Titulo tem termo de TI (passa is_it_title) e
    nenhum termo real de MINHA_STACK — so a falha do bypass VIP antigo faria
    essa vaga ser alertada."""
    vaga = make_vaga(
        company="Acme",
        title="Desenvolvedor - Internship Program",
        description="Precisamos de experiência prévia em atendimento, sem tecnologias específicas.",
    )
    _, sent_calls, _ = setup_run(monkeypatch, tmp_path, [vaga])

    main_module.run(debug=False)

    assert sent_calls == []


def test_run_skips_vaga_with_formacao_deadline_before_target_year(monkeypatch, tmp_path):
    vaga = make_vaga(description="Java e Spring Boot. Formatura até dez/2026.")
    _, sent_calls, _ = setup_run(monkeypatch, tmp_path, [vaga])

    main_module.run(debug=False)

    assert sent_calls == []


def test_run_rate_limits_between_real_sends(monkeypatch, tmp_path):
    vagas = [make_vaga(external_id="1"), make_vaga(external_id="2", url="https://example.com/2")]
    db_path = str(tmp_path / "vagas.db")
    monkeypatch.setattr(main_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "ATS_EXPORT_PATH", str(tmp_path / "vagas_ats.md"))
    monkeypatch.setattr(main_module.GupyScraper, "search", lambda self, term: list(vagas))
    monkeypatch.setattr(
        main_module, "datetime", type("_FixedDatetime", (), {"now": staticmethod(lambda tz: NOW)})
    )
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123")
    monkeypatch.setattr(main_module, "send_message", lambda token, chat_id, text: None)

    sleep_calls = []
    monkeypatch.setattr(main_module.time, "sleep", lambda s: sleep_calls.append(s))

    main_module.run(debug=False)

    assert sleep_calls == [main_module.MIN_SECONDS_BETWEEN_SENDS] * 2
