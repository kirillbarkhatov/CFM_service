from django.db import models
from django.utils import timezone


class Status(models.Model):
    """Справочник статусов ДДС (например: Бизнес, Личное, Налог и т.д.)."""

    name = models.CharField("Название статуса", max_length=64, unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    """Справочник типов движения денежных средств (например: Пополнение, Списание и т.д.)."""

    name = models.CharField("Название типа", max_length=64, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория ДДС, привязанная к определённому типу (Type)."""

    name = models.CharField("Название категории", max_length=64)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="categories", verbose_name="Тип")

    class Meta:
        unique_together = ("name", "type")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class SubCategory(models.Model):
    """Подкатегория ДДС, привязанная к определённой категории (Category)."""

    name = models.CharField("Название подкатегории", max_length=64)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Категория"
    )

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlow(models.Model):
    """Основная модель записи движения денежных средств."""

    created_at = models.DateField("Дата создания", default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField("Сумма (₽)", max_digits=12, decimal_places=2)
    comment = models.TextField("Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "ДДС запись"
        verbose_name_plural = "ДДС записи"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.created_at} | {self.status} | {self.type} | {self.category} | {self.subcategory} | {self.amount}₽"
        )
