# Generated by Django 3.2.3 on 2025-02-26 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='text_url',
            new_name='image_url',
        ),
    ]
