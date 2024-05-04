from django.urls import path

from . import views

app_name = "budget"
urlpatterns = [
    path("", views.main, name="main"),
    path('createexpense', views.createExpense, name='createexpense'),
    path("updateexpense", views.updateExpense, name="updateexpense"),
    path("deleteexpense", views.deleteExpense, name="deleteexpense"),
    path("createchartdata", views.createChartData, name="createchartdata")
]