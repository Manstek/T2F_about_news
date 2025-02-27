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

    tags = models.ManyToManyField(
        Tag,
        related_name='news',
        verbose_name='Тэги')

    content = models.JSONField(verbose_name='Контент')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'
        ordering = ('pub_date',)
        default_related_name = 'news'

    # def __str__(self):
    #     return self.pk


class Notification(models.Model):
    """Модель, представляющая уведомления в телеграмме."""
