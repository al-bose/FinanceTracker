from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login


def main(request):
   return render(request, "home/homepage.html")