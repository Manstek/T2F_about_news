import requests
import os

from django.shortcuts import get_object_or_404
from celery import shared_task, chain


from .compress_news_utils import fetch_article_text
from blog.models import Tag, News, ShortNews

AMOUNT_NEWS = 2


@shared_task
def fetch_news_by_tags():
    """Получение новостей через API."""
    tags = Tag.objects.all()
    api_key = '88a6f5df0c6748d98d7de8006b18fffc'  # TODO убрать в .env
    # api_key = os.getenv('api_key', 'default_key')
    base_url = 'https://newsapi.org/v2/everything'
    news_items = []

    for tag in tags:
        params = {
            'q': tag.name,
            'apiKey': api_key,
            'language': 'ru',
            'pageSize': AMOUNT_NEWS,  # Количество новостей на один тег
        }
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for article in articles:
                    article['tag'] = tag
                    news_items.append(article)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе для тега {tag}: {e}")
        except ValueError as e:
            print(f"Ошибка при обработке JSON для тега {tag}: {e}")
    news_objects = []
    for news in news_items:
        if not News.objects.filter(news_url=news['url']).exists():
            news_objects.append(
                News(
                    tag=news['tag'],
                    title=news['title'],
                    description=news['description'],
                    news_url=news['url'],
                    image_url=news['urlToImage'],
                    pub_date=news['publishedAt']
                )
            )
    # created_news = News.objects.bulk_create(news_objects)

    # news_ids = [news.id for news in created_news]

    news_ids = []
    for news in news_items:
        if not News.objects.filter(news_url=news['url']).exists():
            news_obj = News.objects.create(
                tag=news['tag'],
                title=news['title'],
                description=news['description'],
                news_url=news['url'],
                image_url=news['urlToImage'],
                pub_date=news['publishedAt']
            )
            news_ids.append(news_obj.id)

    if news_ids:
        compress_news.delay(news_ids)

    return news_ids


@shared_task
def compress_news(news_ids):
    """Сжатие новостей."""
    short_news = []
    for news_id in news_ids:
        news = get_object_or_404(News, id=news_id)
        news_text = fetch_article_text(news.news_url)
        short_news.append(
            ShortNews(
                news=news,
                text=news_text
            )
        )
    ShortNews.objects.bulk_create(short_news)

    return len(short_news)
