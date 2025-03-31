import os

from django.shortcuts import get_object_or_404
from celery import shared_task


from .compress_news_utils import fetch_article_text, fetch_news_from_api
from apps.blog.models import Tag, News, ShortNews

AMOUNT_NEWS = 2


@shared_task
def fetch_news_by_tags():
    """Получение новостей через API."""
    tags = Tag.objects.all()
    api_key = os.getenv('API_KEY_NEWS', 'DEFAULT_KEY')
    news_items = []

    for tag in tags:
        articles = fetch_news_from_api(tag, api_key)
        for article in articles:
            article['tag'] = tag
            news_items.append(article)

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

    created_news = News.objects.bulk_create(news_objects)
    news_ids = [news.id for news in created_news]

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
