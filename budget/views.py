from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Expenses
from django.urls import reverse
from decimal import Decimal

# Create your views here.

@login_required
def main(request):
    expenses = Expenses.objects.filter(user_id=request.user.id)
    context = {
        'expenses': expenses,
        'types': Expenses.TYPE_CHOICES
        }

    return render(request, 'budget/index.html', context)

@login_required
def createExpense(request):
    if request.method == "POST":
        expense = Expenses(type = request.POST['type'], user = request.user, date = request.POST["date"], amount = request.POST["amount"], description = request.POST['description'])
        expense.save()
        return HttpResponseRedirect(reverse("budget:main"))
    else:
        context = {
            "types" : Expenses.TYPE_CHOICES
        }
        return render(request, "budget/createexpense.html", context)


@login_required
def updateExpense(request):

    existing_expense_query = Expenses.objects.filter(id= request.POST['updateExpense'])
    print(request)

    if existing_expense_query:
        existing_expense = existing_expense_query.first()
        existing_expense.description = request.POST["description"]
        existing_expense.amount = Decimal(request.POST["amount"])
        existing_expense.type = request.POST["type"]
        existing_expense.date = request.POST["date"]
        existing_expense.save()

    return HttpResponseRedirect(reverse("budget:main")) 

@login_required
def deleteExpense(request):
    eexisting_expense_query = Expenses.objects.filter(id= request.POST['deleteExpense'])
    print(request)
    if eexisting_expense_query:
        existing_expense = eexisting_expense_query.first()
        existing_expense.delete()
    return HttpResponseRedirect(reverse("budget:main")) 