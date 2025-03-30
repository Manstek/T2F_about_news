from django.db import models
from django.contrib.auth.models import AbstractUser

MAX_LENGTH_NAME = 20
MAX_LENGTH_ROLE = 50
ROLES = [
    ('user', 'user'),
    ('admin', 'admin')
]


class Tag(models.Model):
    """Модель тегов, используемых для новостей."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
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
    """Модель представляющая пользователя."""

    tags = models.ManyToManyField(
        Tag,
        related_name='users',
        blank=True,
        verbose_name='Тэги',
        through='UserTag')

    telegram_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        verbose_name='Уникальный индентификатор telegram')
    role = models.CharField(
        choices=ROLES,
        default='user',
        max_length=MAX_LENGTH_ROLE,
        verbose_name='Роль')
    avatar = models.ImageField(upload_to='users/avatar/',
                               null=True, default=None,
                               verbose_name='Аватарка')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserTag(models.Model):
    """Промежуточная таблица для связи M2M."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'тег пользователя'
        verbose_name_plural = 'Теги пользователей'

    def __str__(self):
        return f'Тег - {self.tag.name} пользователя {self.user.username}'
