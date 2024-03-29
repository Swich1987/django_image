# Generated by Django 5.0 on 2024-01-06 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("file", models.ImageField(upload_to="images/")),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Annotation",
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
                ("class_id", models.CharField(max_length=100)),
                ("shape", models.JSONField()),
                ("tags", models.JSONField()),
                ("meta", models.JSONField()),
                ("relations", models.JSONField(blank=True, null=True)),
                ("surface", models.JSONField(blank=True, null=True)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="annotations",
                        to="dent_image_api.image",
                    ),
                ),
            ],
        ),
    ]
