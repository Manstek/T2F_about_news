# Generated by Django 5.1.7 on 2025-03-29 15:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100, verbose_name='Источник')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('news_url', models.URLField(db_index=True, verbose_name='Ссылка на новость')),
                ('image_url', models.URLField(verbose_name='Ссылка на фото новости')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации новости')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='users.tag')),
            ],
            options={
                'verbose_name': 'новость',
                'verbose_name_plural': 'Новости',
                'ordering': ('pub_date',),
                'default_related_name': 'news',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Изображение')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'Посты',
                'ordering': ('-pub_date',),
                'default_related_name': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('pub_date',),
                'default_related_name': 'comments',
            },
        ),
        migrations.CreateModel(
            name='ShortNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Главная мысль сжатой новости')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации новости')),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.news')),
            ],
            options={
                'verbose_name': 'сжатая новость',
                'verbose_name_plural': 'Сжатые новости',
                'ordering': ('pub_date',),
                'default_related_name': 'short_news',
            },
        ),
    ]
