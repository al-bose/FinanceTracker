from django.shortcuts import render
from django.contrib.auth.models import User


def main(request):
   return render(request, "home/homepage.html")

def createUser(request):
    if request.method == "POST":
        user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
        user.first_name = request.POST["firstname"]
        user.last_name = request.POST["lastname"]
        user.save()
        return render(request, "home/login.html")
    else:
        return render(request, "home/create_user.html")

