from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.main, name="main"),
    path("createposition", views.createPosition, name="createposition"),
    path("updateposition", views.updatePosition, name="updateposition"),
    path("deleteposition", views.deletePosition, name="deleteposition")
]