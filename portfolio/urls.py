from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.main, name="main"),
    path("create-position", views.createPosition, name="create-position"),
    path("update-position", views.updatePosition, name="update-position"),
    path("delete-position", views.deletePosition, name="delete-position")
]