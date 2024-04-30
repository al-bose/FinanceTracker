from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.main, name="main"),
    path("createposition", views.createPosition, name="createposition")
]