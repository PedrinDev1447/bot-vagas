from dataclasses import replace

import httpx
import pytest

from src.alerter.telegram import format_message, send_message
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


def test_format_message_includes_essentials():
    text = format_message(BASE_VAGA, ["java", "spring boot"])

    assert "Desenvolvedor Java Junior" in text
    assert "Acme" in text
    assert "hybrid" in text
    assert "São Paulo" in text
    assert "java" in text and "spring boot" in text
    assert "https://example.com/job/1" in text


def test_format_message_remote_job_shows_remoto_label():
    vaga = replace(BASE_VAGA, workplace_type="remote", city="", state="")
    text = format_message(vaga, ["aws"])
    assert "Remoto" in text


def test_format_message_empty_terms_with_vip_explains_bypass():
    """Vaga alertada so por bypass de empresa VIP (spec 0002) nao pode deixar
    "Match: " em branco — precisa explicar o motivo do alerta."""
    text = format_message(BASE_VAGA, [], vip=True)
    assert "Match: " in text
    assert "empresa VIP" in text
    assert "VIP" in text.splitlines()[0]


def test_format_message_non_vip_unaffected_by_new_param():
    text = format_message(BASE_VAGA, ["java"], vip=False)
    assert "VIP" not in text


def test_send_message_posts_token_and_payload(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})

        class FakeResponse:
            def raise_for_status(self):
                pass

        return FakeResponse()

    monkeypatch.setattr("src.alerter.telegram.httpx.post", fake_post)

    send_message("TOKEN123", "999", "hello")

    assert len(calls) == 1
    assert calls[0]["url"] == "https://api.telegram.org/botTOKEN123/sendMessage"
    assert calls[0]["json"] == {"chat_id": "999", "text": "hello"}


def test_send_message_propagates_http_errors(monkeypatch):
    def fake_post(url, json, timeout):
        request = httpx.Request("POST", url)
        response = httpx.Response(429, request=request)

        class FakeResponse:
            def raise_for_status(self):
                raise httpx.HTTPStatusError("429 rate limited", request=request, response=response)

        return FakeResponse()

    monkeypatch.setattr("src.alerter.telegram.httpx.post", fake_post)

    with pytest.raises(httpx.HTTPStatusError):
        send_message("TOKEN123", "999", "hello")
