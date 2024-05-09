from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.main, name="main"),
    path("create-position", views.createPosition, name="create-position"),
    path("update-position/<int:updateId>", views.updatePosition, name="update-position"),
    path("delete-position/<int:deleteId>", views.deletePosition, name="delete-position")
]