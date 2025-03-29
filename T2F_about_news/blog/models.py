from django.db import models

from users.models import User, Tag


class Post(models.Model):
    """Модель, представляющая публикацию пользователя."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор')

    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    image = models.ImageField(
        blank=True,
        verbose_name='Изображение')

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель, представляющая комментарий пользователя к публикации."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор')

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий к посту - {self.post}'


class News(models.Model):
    """Модель, представляющая новость, полученную с API."""

    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL,
                            related_name='news', null=True)

    source = models.CharField(max_length=100, verbose_name='Источник')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    news_url = models.URLField(verbose_name='Ссылка на новость', db_index=True)
    image_url = models.URLField(verbose_name='Ссылка на фото новости')
    pub_date = models.DateTimeField(verbose_name='Дата публикации новости')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'
        ordering = ('pub_date',)
        default_related_name = 'news'


class ShortNews(models.Model):
    """Модель, представляющая сжатую новость, полученную с API."""

    news = models.OneToOneField(News, on_delete=models.CASCADE)

    text = models.TextField(verbose_name='Главная мысль сжатой новости')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации новости', auto_now_add=True)

    class Meta:
        verbose_name = 'сжатая новость'
        verbose_name_plural = 'Сжатые новости'
        ordering = ('pub_date',)
        default_related_name = 'short_news'


class Notification(models.Model):
    """Модель, представляющая уведомления в телеграмме."""
