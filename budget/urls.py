from django.urls import path

from . import views
from budget.views import ExpenseListView

app_name = "budget"
urlpatterns = [
    path("", views.main, name="main"),
    path('createexpense', views.createExpense, name='createexpense'),
    path("updateexpense/<int:updateId>", views.updateExpense, name='updateexpense'),
    path("deleteexpense/<int:deleteId>", views.deleteExpense, name="deleteexpense"),
    path("createchartdata", views.createChartData, name="createchartdata"),
    path("expenses", ExpenseListView.as_view(), name='expenses')
]