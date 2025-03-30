import json
import os

from newspaper import Article
import requests
from requests.exceptions import RequestException


API_KEY_DEEPSEAK = os.getenv('API_KEY_DEEPSEAK', 'DEFAULT_KEY')
MODEL = os.getenv('MODEL', 'DEFAULT_KEY')
API_URL = os.getenv('API_URL', 'DEFAULT_KEY')
AMOUNT_NEWS = 2
SYSTEM_CONTENT = (
    'Ты — инструмент для сжатия текста.'
    'Твоя задача — сокращать текст так, '
    'чтобы его можно было прочитать за 10-15 секунд и понять главное.'
    'Оставляй только ключевые моменты, удаляя всё лишнее.'
    'Максимум 100 слов и 2 предложения.'
)
USER_CONTENT = (
    'Сократи текст, выделив главное, '
    'чтобы это можно было прочитать за 10-20 секунд '
    '(максимум 2 предложения и 100 слов, но старайся как можно меньше слов)'
    ', вот текст:'
)
TIMEOUT = 30
LANGUAGE = 'ru'


def fetch_article_text(url):
    """Извлекает текст статьи по указанному URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        raise Exception(
            f"Не удалось обработать статью по URL {url}: {str(e)}")


def process_content(content):
    """Удаляет теги <think> и </think> из текста."""
    return content.replace('<think>', '').replace('</think>', '')


def chat(prompt):
    """Отправляет запрос к модели и возвращает ответ."""
    headers = {
        "Authorization": f"Bearer {API_KEY_DEEPSEAK}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_CONTENT
            },
            {
                "role": "user",
                "content": f'{USER_CONTENT} {prompt}'
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=TIMEOUT
        )
        response.raise_for_status()
    except RequestException as e:
        raise Exception(f"Ошибка при запросе к API: {str(e)}")

    try:
        response_data = response.json()
        if "choices" not in response_data:
            raise Exception(
                "Некорректный формат ответа API: отсутствует ключ 'choices'")

        content = response_data["choices"][0]["message"].get("content", "")
        return process_content(content)
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        raise Exception(f"Ошибка при обработке ответа API: {str(e)}")


def fetch_news_from_api(tag, api_key):
    """Отправка запроса к API и получение новостей по тегу."""
    base_url = os.getenv('API_NEWS_URL', 'DEFAULT_KEY')
    params = {
        'q': tag.name,
        'apiKey': api_key,
        'language': LANGUAGE,
        'pageSize': AMOUNT_NEWS,  # Количество новостей на один тег
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get('articles', [])
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при запросе для тега {tag}: {e}")
    except ValueError as e:
        raise Exception(f"Ошибка при обработке JSON для тега {tag}: {e}")
