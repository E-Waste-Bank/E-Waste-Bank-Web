# Generated by Django 4.1 on 2022-11-02 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tips_and_tricks', '0004_remove_tipsandtrick_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipsandtrick',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
