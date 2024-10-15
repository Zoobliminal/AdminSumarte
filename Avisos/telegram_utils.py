from django.conf import settings
import requests


def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # O 'HTML' si lo configuramos como HTML
    }
    response = requests.post(url, data=payload)
    return response.json()