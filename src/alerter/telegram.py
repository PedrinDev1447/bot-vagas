import httpx

from src.scraper.base import Vaga

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def format_message(vaga: Vaga, matched_terms: list[str]) -> str:
    """Mensagem enxuta por vaga (D2/D14 completo — script de apresentacao
    pronto pra colar — fica pra depois; aqui e so titulo/empresa/link)."""
    location = vaga.city or "Remoto"
    return (
        f"{vaga.title}\n"
        f"{vaga.company} — {vaga.workplace_type} ({location})\n"
        f"Match: {', '.join(matched_terms)}\n"
        f"{vaga.url}"
    )


def send_message(token: str, chat_id: str, text: str) -> None:
    url = TELEGRAM_API_URL.format(token=token)
    response = httpx.post(url, json={"chat_id": chat_id, "text": text}, timeout=20.0)
    response.raise_for_status()
