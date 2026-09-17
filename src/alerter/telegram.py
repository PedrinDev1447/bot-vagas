import httpx

from src.scraper.base import Vaga

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def format_message(vaga: Vaga, matched_terms: list[str], vip: bool = False) -> str:
    """Mensagem enxuta por vaga (D2/D14 completo — script de apresentacao
    pronto pra colar — fica pra depois; aqui e so titulo/empresa/link).
    matched_terms pode vir vazio quando a vaga so entrou por bypass de
    empresa VIP (spec 0002) — nesse caso o rotulo explica o motivo do alerta
    em vez de deixar "Match: " em branco."""
    location = vaga.city or "Remoto"
    match_label = ", ".join(matched_terms) if matched_terms else "empresa VIP (sem termo de stack)"
    title = f"{vaga.title} ⭐VIP" if vip else vaga.title
    return (
        f"{title}\n"
        f"{vaga.company} — {vaga.workplace_type} ({location})\n"
        f"Match: {match_label}\n"
        f"{vaga.url}"
    )


def send_message(token: str, chat_id: str, text: str) -> None:
    url = TELEGRAM_API_URL.format(token=token)
    response = httpx.post(url, json={"chat_id": chat_id, "text": text}, timeout=20.0)
    response.raise_for_status()
