from django.urls import path

from . import views
from budget.views import ExpenseListView

app_name = "budget"
urlpatterns = [
    path("", views.main, name="main"),
    path('create-expense', views.createExpense, name='create-expense'),
    path("update-expense/<int:updateId>", views.updateExpense, name='update-expense'),
    path("delete-expense/<int:deleteId>", views.deleteExpense, name="delete-expense"),
    path("create-chart-data", views.createChartData, name="create-chart-data"),
    path("expenses", ExpenseListView.as_view(), name='expenses')
]