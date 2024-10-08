# Generated by Django 5.1 on 2024-08-17 19:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogRequest",
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
                ("url", models.CharField(max_length=255)),
                ("status_code", models.IntegerField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("method", models.CharField(max_length=10)),
                ("payload", models.TextField(blank=True, null=True)),
                ("response", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
