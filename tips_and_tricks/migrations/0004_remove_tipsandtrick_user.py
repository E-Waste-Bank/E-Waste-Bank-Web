# Generated by Django 4.1 on 2022-11-01 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips_and_tricks', '0003_tipsandtrick_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipsandtrick',
            name='user',
        ),
    ]
