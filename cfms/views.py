from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from cfms.forms import CashFlowForm, CategoryForm, StatusForm, SubCategoryForm, TypeForm
from cfms.models import CashFlow, Category, Status, SubCategory, Type


class CashFlowListView(ListView):
    model = CashFlow
    template_name = "cfms/cashflow_list.html"
    context_object_name = "cashflows"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        # Фильтрация по параметрам
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        status = self.request.GET.get("status")
        type_ = self.request.GET.get("type")
        category = self.request.GET.get("category")
        subcategory = self.request.GET.get("subcategory")
        if date_from:
            qs = qs.filter(created_at__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__lte=date_to)
        if status:
            qs = qs.filter(status_id=status)
        if type_:
            qs = qs.filter(type_id=type_)
        if category:
            qs = qs.filter(category_id=category)
        if subcategory:
            qs = qs.filter(subcategory_id=subcategory)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["types"] = Type.objects.all()
        context["categories"] = Category.objects.all()
        context["subcategories"] = SubCategory.objects.all()
        return context


class CashFlowCreateView(CreateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = "cfms/cashflow_form.html"
    success_url = reverse_lazy("cfms:cashflow_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "GET":
            # Пробуем вытащить type из GET-параметра, если он был
            type_id = self.request.GET.get("type")
            if type_id:
                kwargs["initial"] = {"type": type_id}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = Type.objects.all()
        context["categories"] = Category.objects.select_related("type").all()
        context["subcategories"] = SubCategory.objects.select_related("category").all()
        return context


class CashFlowUpdateView(UpdateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = "cfms/cashflow_form.html"
    success_url = reverse_lazy("cfms:cashflow_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = Type.objects.all()
        context["categories"] = Category.objects.select_related("type").all()
        context["subcategories"] = SubCategory.objects.select_related("category").all()
        return context

class CashFlowDeleteView(DeleteView):
    model = CashFlow
    template_name = "cfms/cashflow_confirm_delete.html"
    success_url = reverse_lazy("cfms:cashflow_list")


class DirectoryManageView(View):
    template_name = "cfms/directory_manage.html"

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get("action")
        obj_type = request.POST.get("object_type")
        obj_id = request.POST.get("object_id")  # может быть пустым при добавлении

        # Определим модель и форму по типу
        model_map = {
            "status": (Status, StatusForm),
            "type": (Type, TypeForm),
            "category": (Category, CategoryForm),
            "subcategory": (SubCategory, SubCategoryForm),
        }

        if obj_type not in model_map:
            return redirect("cfms:directory_manage")  # safety fallback

        model_class, form_class = model_map[obj_type]

        # Удаление
        if action == "delete":
            instance = get_object_or_404(model_class, pk=obj_id)
            instance.delete()
            return redirect("cfms:directory_manage")

        # Добавление или редактирование
        instance = None
        if action == "edit" and obj_id:
            instance = get_object_or_404(model_class, pk=obj_id)

        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("cfms:directory_manage")

        # Если ошибка — вернём форму с ошибками
        context = self.get_context_data()
        context[f"{obj_type}_form"] = form
        return render(request, self.template_name, context)

    def get_context_data(self):
        return {
            "statuses": Status.objects.all(),
            "types": Type.objects.all(),
            "categories": Category.objects.select_related("type").all(),
            "subcategories": SubCategory.objects.select_related("category").all(),
            "status_form": StatusForm(),
            "type_form": TypeForm(),
            "category_form": CategoryForm(),
            "subcategory_form": SubCategoryForm(),
        }


def categories_by_type(request, type_id):
    categories = Category.objects.filter(type_id=type_id).values("id", "name")
    return JsonResponse(list(categories), safe=False)


def subcategories_by_category(request, category_id):
    subcategories = SubCategory.objects.filter(category_id=category_id).values("id", "name")
    return JsonResponse(list(subcategories), safe=False)