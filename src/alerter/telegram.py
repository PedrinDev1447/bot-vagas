import httpx

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def send_message(token: str, chat_id: str, text: str) -> None:
    url = TELEGRAM_API_URL.format(token=token)
    response = httpx.post(url, json={"chat_id": chat_id, "text": text}, timeout=20.0)
    response.raise_for_status()
