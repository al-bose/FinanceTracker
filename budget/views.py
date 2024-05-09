import calendar
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Expenses
from django.urls import reverse
from decimal import Decimal
import datetime
from timedelta import Timedelta
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@login_required
def main(request):

    #default to querying expenses from this current month
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    _, num_days = calendar.monthrange(current_year, current_month)

    first_day = datetime.date(current_year, current_month, 1)
    last_day = datetime.date(current_year, current_month, num_days)

    expenses = Expenses.objects.filter(user_id=request.user.id).filter(date__gte = first_day).filter(date__lte = last_day)
    total = 0

    data = {}

    for type in Expenses.TYPE_CHOICES.keys():
        data[type] = 0

    for expense in expenses:
        data[expense.type] += expense.amount
        total += expense.amount

    context = {
        'expenses': expenses,
        'types': Expenses.TYPE_CHOICES,
        'data': data,
        'total': total
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
        return render(request, "budget/create_expense.html", context)


@login_required
def updateExpense(request, updateId):
    expense = Expenses.objects.filter(user_id = request.user.id).filter(id=updateId).get()
    if request.method == "POST":
        expense.description = request.POST["description"]
        expense.amount = Decimal(request.POST["amount"])
        expense.type = request.POST["type"]
        expense.date = request.POST["date"]
        expense.save()
        return HttpResponseRedirect(reverse("budget:expenses")) 
    else:
        context = {
            "types" : Expenses.TYPE_CHOICES,
            "expense" : expense
        }
        return render(request, "budget/update_expense.html", context)
        

@login_required
def deleteExpense(request, deleteId):
    expense = Expenses.objects.filter(user_id = request.user.id).filter(id=deleteId).get()
    expense.delete()
    return HttpResponseRedirect(reverse("budget:expenses")) 

@login_required
def createChartData(request):
    chartLabel = "Total Spent This Month"

    #default to querying expenses from this current month
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    _, num_days = calendar.monthrange(current_year, current_month)

    first_day = datetime.date(current_year, current_month, 1)
    last_day = datetime.date(current_year, current_month, num_days)

    expenses = Expenses.objects.filter(user_id=request.user.id).filter(date__gte = first_day).filter(date__lte = last_day)

    data = {}

    for type in Expenses.TYPE_CHOICES.keys():
        data[type] = 0

    for expense in expenses:
        data[expense.type] += expense.amount

    labels = list(data.keys())
    data = {
        "Labels": labels,
        "chartLabel": chartLabel,
        "chartdata": [data[type] for type in labels]
    }

    return JsonResponse(data)


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expenses
    paginate_by = 10

    def get_queryset(self):
       return Expenses.objects.filter(user_id=self.request.user.id).order_by('-date')

    