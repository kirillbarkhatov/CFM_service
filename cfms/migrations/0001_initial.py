# Generated by Django 5.2.1 on 2025-05-31 20:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True, verbose_name="Категория")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True, verbose_name="Статус")),
            ],
        ),
        migrations.CreateModel(
            name="Type",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True, verbose_name="Тип")),
            ],
        ),
        migrations.CreateModel(
            name="SubCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, verbose_name="Подкатегория")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategories",
                        to="cfms.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подкатегория",
                "verbose_name_plural": "Подкатегории",
                "unique_together": {("name", "category")},
            },
        ),
        migrations.CreateModel(
            name="CashFlow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateField(default=django.utils.timezone.now, verbose_name="Дата создания")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Сумма (₽)")),
                ("comment", models.TextField(blank=True, null=True, verbose_name="Комментарий")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="cfms.category", verbose_name="Категория"
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="cfms.status", verbose_name="Статус"
                    ),
                ),
                (
                    "subcategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="cfms.subcategory", verbose_name="Подкатегория"
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="cfms.type", verbose_name="Тип"),
                ),
            ],
            options={
                "verbose_name": "ДДС запись",
                "verbose_name_plural": "ДДС записи",
                "ordering": ["-created_at"],
            },
        ),
    ]
