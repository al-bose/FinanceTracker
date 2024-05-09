from django.urls import include,path
from django.contrib.auth import views as auth_views

from . import views

app_name = "home"
urlpatterns = [
    path("", views.main, name="main"),
    #path("login", views.login, name="login")
    path("login/", auth_views.LoginView.as_view(template_name="home/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="home/homepage.html"), name="logout"),
    path("create-user/", views.createUser, name="create-user"),
]