# Generated by Django 4.1 on 2022-10-28 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips_and_tricks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tipsandtrick',
            old_name='author',
            new_name='article_url',
        ),
        migrations.RenameField(
            model_name='tipsandtrick',
            old_name='url_article',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='tipsandtrick',
            old_name='url_image',
            new_name='source',
        ),
    ]
