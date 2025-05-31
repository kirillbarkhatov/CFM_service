from django import forms

from cfms.models import CashFlow, Category, Status, SubCategory, Type


class CashFlowForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей ДДС.
    Реализует зависимость: категория фильтруется по типу, подкатегория по категории.
    Валидация: сумма — только целое число, категории и подкатегории соответствуют выбранным типу/категории.
    """

    class Meta:
        model = CashFlow
        fields = ["created_at", "status", "type", "category", "subcategory", "amount", "comment"]
        widgets = {
            "created_at": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "inputmode": "numeric", "step": "1", "min": "0"}
            ),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["category"].initial = self.instance.category
            self.fields["subcategory"].initial = self.instance.subcategory

        for field in ["status", "type", "category", "subcategory"]:
            self.fields[field].widget.attrs["class"] = "form-select"

        # Загружаем все, фильтрация в JS
        self.fields["category"].queryset = Category.objects.select_related("type").all()
        self.fields["subcategory"].queryset = SubCategory.objects.select_related("category").all()

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount % 1 != 0:
            raise forms.ValidationError("Введите целое число.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        type_ = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if category and type_ and category.type_id != type_.id:
            self.add_error("category", "Категория не относится к выбранному типу.")
        if subcategory and category and subcategory.category_id != category.id:
            self.add_error("subcategory", "Подкатегория не относится к выбранной категории.")

        return cleaned_data


class StatusForm(forms.ModelForm):
    """Форма для управления справочником статусов ДДС."""

    class Meta:
        model = Status
        fields = ["name"]


class TypeForm(forms.ModelForm):
    """Форма для управления справочником типов ДДС."""

    class Meta:
        model = Type
        fields = ["name"]


class CategoryForm(forms.ModelForm):
    """Форма для управления справочником категорий ДДС (связана с типом)."""

    class Meta:
        model = Category
        fields = ["name", "type"]


class SubCategoryForm(forms.ModelForm):
    """Форма для управления справочником подкатегорий ДДС (связана с категорией)."""

    class Meta:
        model = SubCategory
        fields = ["name", "category"]
