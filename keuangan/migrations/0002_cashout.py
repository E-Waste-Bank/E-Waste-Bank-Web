# Generated by Django 4.1 on 2022-10-27 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("keuangan", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cashout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("approved", models.BooleanField()),
                ("disbursed", models.BooleanField()),
                (
                    "uang_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="keuangan.keuanganadmin",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]