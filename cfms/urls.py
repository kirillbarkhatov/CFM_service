from django.urls import path

from cfms.apps import CfmsConfig
from cfms.views import (CashFlowCreateView, CashFlowDeleteView, CashFlowListView, CashFlowUpdateView,
                        DirectoryManageView, categories_by_type, subcategories_by_category)

app_name = CfmsConfig.name

urlpatterns = [
    path("", CashFlowListView.as_view(), name="cashflow_list"),
    path("add/", CashFlowCreateView.as_view(), name="cashflow_add"),
    path("edit/<int:pk>/", CashFlowUpdateView.as_view(), name="cashflow_edit"),
    path("delete/<int:pk>/", CashFlowDeleteView.as_view(), name="cashflow_delete"),
    path("directories/", DirectoryManageView.as_view(), name="directory_manage"),
    path("ajax/categories/<int:type_id>/", categories_by_type, name="ajax_categories_by_type"),
    path("ajax/subcategories/<int:category_id>/", subcategories_by_category, name="ajax_subcategories_by_category"),
]
