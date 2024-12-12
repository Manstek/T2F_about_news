from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = [
    ('user', 'user'),
    ('admin', 'admin')
]


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
        choices=ROLES,
        default='user',
        max_length=50,
        verbose_name='Роль')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username