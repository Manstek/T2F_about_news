from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Тэг')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)
        default_related_name = 'tags'

    def __str__(self):
        return self.name


class User(AbstractUser):
    tags = models.ManyToManyField(
        Tag,
        related_name='users',
        blank=True,
        verbose_name='Тэги')

    telegram_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        verbose_name='Уникальный индентификатор telegram')
    role = models.CharField(
        choices=settings.ROLES,
        default='user',
        max_length=50,
        verbose_name='Роль')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Post(models.Model):
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
    # image = models.ImageField(
    #     blank=False,
    #     verbose_name='Изображение')

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
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


class News(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='news',
        verbose_name='Тэги')

    content = models.JSONField(verbose_name='Контент')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    def __str__(self):
        return self.pk


class Notification(models.Model):
    pass
