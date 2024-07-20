import requests

from config.settings import TELEGRAM_API, TELEGRAM_URL


def send_telegram_notice(text, chat_id):
    params = {
        'text': text,
        'chat_id': chat_id,
    }
    response = requests.get(f'{TELEGRAM_URL}{TELEGRAM_API}/sendMessage', params=params)
