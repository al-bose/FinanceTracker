from django.urls import path

from . import views
from .views import PositionListView

app_name = "portfolio"
urlpatterns = [
    path("", views.main, name="main"),
    path("create-position", views.createPosition, name="create-position"),
    path("update-position/<int:updateId>", views.updatePosition, name="update-position"),
    path("delete-position/<int:deleteId>", views.deletePosition, name="delete-position"),
    path("positions/<str:type>", PositionListView.as_view(), name='positions')
]