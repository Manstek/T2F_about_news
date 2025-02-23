import requests


def fetch_news_by_tags(tags):
    """Получение новостей через API."""

    api_key = '88a6f5df0c6748d98d7de8006b18fffc'  # TODO убрать в .env
    base_url = 'https://newsapi.org/v2/everything'
    news_items = []

    for tag in tags:
        params = {
            'q': tag,  # Используем имя тега как ключевое слово для поиска
            'apiKey': api_key,
            'language': 'ru',  # Язык новостей (можно изменить)
            'pageSize': 5,  # Количество новостей на один тег
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            news_items.extend(response.json().get('articles', []))

    return news_items
