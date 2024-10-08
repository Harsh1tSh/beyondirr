# Generated by Django 5.1 on 2024-08-17 21:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_logrequest"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                ("product", models.CharField(max_length=255, unique=True)),
                (
                    "asset_class",
                    models.CharField(
                        choices=[
                            ("Equity", "Equity"),
                            ("Debt", "Debt"),
                            ("Alternate", "Alternate"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date", models.DateField()),
                ("units", models.DecimalField(decimal_places=2, max_digits=10)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "product", "date")},
            },
        ),
    ]
