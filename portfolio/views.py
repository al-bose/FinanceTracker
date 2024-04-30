from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Positions

# Create your views here.

@login_required
def main(request):
    stocks = Positions.objects.filter(user_id=request.user.id)
    context = {"stocks" : stocks}
    return render(request, "portfolio/index.html", context)

@login_required
def createPosition(request):
    if request.method == "POST":
        position = Positions(purchased_date= request.POST["date"], ticker= request.POST["ticker"], quantity= request.POST["quantity"], cost_basis= request.POST["costBasis"])
        position.user = request.user
        position.save()
        return main(request)
    else:
        return render(request, "portfolio/createposition.html")
