from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Positions
import environ
import json
import requests
import datetime
from timedelta import Timedelta
import math
from decimal import Decimal
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@login_required
def main(request):
    stocks = Positions.objects.filter(user_id=request.user.id)

    #only display top 3 stocks for each type on the main page
    roth = stocks.filter(type=Positions.ROTH).order_by("-quantity")[:3]
    individual = stocks.filter(type=Positions.INDIVIDUAL).order_by("-quantity")[:3]
    retirement = stocks.filter(type=Positions.RETIREMENT).order_by("-quantity")[:3]

    #calculate total current value for stock
    total_ticker_prices = {}

    total_type_prices = {
        "current_value": {
            Positions.RETIREMENT : 0,
            Positions.INDIVIDUAL : 0,
            Positions.ROTH : 0,
            Positions.CRYPTO : 0
        },
        "total_cost": {
            Positions.RETIREMENT : 0,
            Positions.INDIVIDUAL : 0,
            Positions.ROTH : 0,
            Positions.CRYPTO : 0
        },
        "percentage_change": {
            Positions.RETIREMENT : 0,
            Positions.INDIVIDUAL : 0,
            Positions.ROTH : 0,
            Positions.CRYPTO : 0
        },
        "change": {
            Positions.RETIREMENT : 0,
            Positions.INDIVIDUAL : 0,
            Positions.ROTH : 0,
            Positions.CRYPTO : 0
        },
        "daily_change": {
            Positions.RETIREMENT : 0,
            Positions.INDIVIDUAL : 0,
            Positions.ROTH : 0,
            Positions.CRYPTO : 0
        },
        "daily_percentage_change": {
            Positions.RETIREMENT : 0,
            Positions.INDIVIDUAL : 0,
            Positions.ROTH : 0,
            Positions.CRYPTO : 0
        }
    }

    total_prices = {
        "current_value": 0,
        "total_cost": 0,
        "percentage_change": 0,
        "change": 0,
        "daily_change": 0,
        "daily_percentage_change": 0
    }

    for stock in stocks:
        data = getTickerData(stock.ticker)

        most_recent_refresh = data["Meta Data"]["3. Last Refreshed"]
        most_recent_entry = data["Time Series (Daily)"][most_recent_refresh]
        most_recent_price = Decimal(most_recent_entry["4. close"])

        days = list(data["Time Series (Daily)"].keys())
        sorted_days = sorted(days, key=lambda x: datetime.datetime.strptime(x, '%Y-%M-%d'), reverse=True)

        second_most_recent_refresh = sorted_days[1]
        second_most_recent_entry = data["Time Series (Daily)"][second_most_recent_refresh]
        second_most_recent_price = Decimal(second_most_recent_entry["4. close"])

        current_value = most_recent_price * stock.quantity
        last_value = second_most_recent_price * stock.quantity
        total_cost = stock.quantity * stock.cost_basis
        percentage_change = (current_value - total_cost)/total_cost * 100
        daily_percentage_change = (current_value - last_value)/last_value * 100

        if stock.ticker in total_ticker_prices.keys():
            total_ticker_prices[stock.ticker][stock.type] = {
                "current_value": round(current_value,2),
                "total_cost": round(total_cost,2),
                "change": round(current_value - total_cost, 2),
                "percentage_change": round(percentage_change, 2),
                "daily_change": round(current_value - last_value),
                "daily_percentage_change": round(daily_percentage_change, 2)
            }
        else:
            total_ticker_prices[stock.ticker] = {
                stock.type : {
                    "current_value": round(current_value,2),
                    "total_cost": round(total_cost,2),
                    "change": round(current_value - total_cost, 2),
                    "percentage_change": round(percentage_change, 2),
                    "daily_change": round(current_value - last_value),
                    "daily_percentage_change": round(daily_percentage_change, 2)
                }
            }
        
        total_type_prices["current_value"][stock.type] += current_value
        total_type_prices["total_cost"][stock.type] += total_cost
        total_type_prices["change"][stock.type] += (current_value - total_cost)
        total_type_prices["daily_change"][stock.type] += (current_value - last_value)

        total_prices["current_value"] += current_value
        total_prices["total_cost"] += total_cost
        total_prices["change"] += (current_value - total_cost)
        total_prices["daily_change"] += (current_value - last_value)

        stock.cost_basis = round(stock.cost_basis, 2)
        stock.quantity = round(stock.quantity, 2)

    for type in Positions.TYPE_CHOICES.keys():
        if total_type_prices["total_cost"][type] > 0:
            total_type_prices["percentage_change"][type] = round((total_type_prices["current_value"][type] - total_type_prices["total_cost"][type])/total_type_prices["total_cost"][type] * 100,2)
            total_type_prices["daily_percentage_change"][type] = round((total_type_prices["daily_change"][type])/(total_type_prices["current_value"][type] - total_type_prices["daily_change"][type])* 100,2)
            total_type_prices["current_value"][type] = round(total_type_prices["current_value"][type],2)
            total_type_prices["total_cost"][type] = round(total_type_prices["total_cost"][type],2)
            total_type_prices["change"][type] = round(total_type_prices["change"][type],2)
            total_type_prices["daily_change"][type] = round(total_type_prices["change"][type], 2)

    if total_prices["total_cost"] > 0:
        total_prices["percentage_change"] = round((total_prices["current_value"] - total_prices["total_cost"])/total_prices["total_cost"] * 100,2)
    if total_prices["current_value"] - total_prices["daily_change"] !=0:
        total_prices["daily_percentage_change"] = round((total_prices["daily_change"])/(total_prices["current_value"] - total_prices["daily_change"])* 100,2)

    total_prices["current_value"] = round(total_prices["current_value"],2)
    total_prices["total_cost"] = round(total_prices["total_cost"],2)
    total_prices["change"] = round(total_prices["change"],2)
    total_prices["daily_change"] = round(total_prices["daily_change"], 2)

    context = {"total_ticker_prices": total_ticker_prices, "total_type_prices": total_type_prices, "total_prices": total_prices,  "roth": roth, "individual": individual, "retirement": retirement}
    return render(request, "portfolio/index.html", context)

@login_required
def createPosition(request):
    if request.method == "POST":
        existing_position_query = Positions.objects.filter(user_id = request.user.id).filter(ticker = request.POST["ticker"]).filter(type = request.POST["type"])

        if existing_position_query:
            existing_position = existing_position_query.first()
            existing_position.cost_basis = ((existing_position.quantity * existing_position.cost_basis) + (Decimal(request.POST["quantity"]) * Decimal(request.POST["costBasis"])))/(existing_position.quantity + Decimal(request.POST["quantity"]))
            existing_position.quantity += Decimal(request.POST["quantity"])
            existing_position.save()
        else:
            position = Positions(type = request.POST["type"], ticker= request.POST["ticker"], quantity= request.POST["quantity"], cost_basis= request.POST["costBasis"])
            position.user = request.user
            position.save()

        return HttpResponseRedirect(reverse("portfolio:main"))
    else:
        env = environ.Env()
        environ.Env.read_env()   
        context = {
            "api_key" : env("API_KEY"),
            "types" : Positions.TYPE_CHOICES
        }
        return render(request, "portfolio/create_position.html", context)
    
@login_required
def updatePosition(request, updateId):
    position = Positions.objects.filter(user_id = request.user.id).filter(id=updateId).get()

    if request.method == "POST":
        position.cost_basis = Decimal(request.POST["costBasis"])
        position.quantity = Decimal(request.POST["quantity"])
        position.save()
        return HttpResponseRedirect(reverse("portfolio:main")) 
    else:
        context = {
            "position": position
        }
        return render(request, "portfolio/update_position.html", context)


@login_required
def deletePosition(request, deleteId):
    position = Positions.objects.filter(user_id = request.user.id).filter(id=deleteId).get()
    position.delete()
    return HttpResponseRedirect(reverse("portfolio:main")) 

class PositionListView(LoginRequiredMixin, ListView):
    model = Positions
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        total_ticker_prices = {}

        for stock in context["object_list"]:
            data = getTickerData(stock.ticker)

            most_recent_refresh = data["Meta Data"]["3. Last Refreshed"]
            most_recent_entry = data["Time Series (Daily)"][most_recent_refresh]
            most_recent_price = Decimal(most_recent_entry["4. close"])

            days = list(data["Time Series (Daily)"].keys())
            sorted_days = sorted(days, key=lambda x: datetime.datetime.strptime(x, '%Y-%M-%d'), reverse=True)

            second_most_recent_refresh = sorted_days[1]
            second_most_recent_entry = data["Time Series (Daily)"][second_most_recent_refresh]
            second_most_recent_price = Decimal(second_most_recent_entry["4. close"])

            current_value = most_recent_price * stock.quantity
            last_value = second_most_recent_price * stock.quantity
            total_cost = stock.quantity * stock.cost_basis
            percentage_change = (current_value - total_cost)/total_cost * 100
            daily_percentage_change = (current_value - last_value)/last_value * 100

            if stock.ticker in total_ticker_prices.keys():
                total_ticker_prices[stock.ticker][stock.type] = {
                    "current_value": round(current_value,2),
                    "total_cost": round(total_cost,2),
                    "change": round(current_value - total_cost, 2),
                    "percentage_change": round(percentage_change, 2),
                    "daily_change": round(current_value - last_value),
                    "daily_percentage_change": round(daily_percentage_change, 2)
                }
            else:
                total_ticker_prices[stock.ticker] = {
                    stock.type : {
                        "current_value": round(current_value,2),
                        "total_cost": round(total_cost,2),
                        "change": round(current_value - total_cost, 2),
                        "percentage_change": round(percentage_change, 2),
                        "daily_change": round(current_value - last_value),
                        "daily_percentage_change": round(daily_percentage_change, 2)
                    }
                }

        context["type"] = self.kwargs["type"]
        context["total_ticker_prices"] = total_ticker_prices
        return context
    def get_queryset(self):
       return Positions.objects.filter(user_id=self.request.user.id).filter(type=self.kwargs["type"]).order_by('-quantity')
    

def getTickerData(ticker):
    env = environ.Env()
    environ.Env.read_env()

    #response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey='+env("API_KEY"))
    #data = response.json()

    data = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "TSLA",
            "3. Last Refreshed": "2024-05-03",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2024-05-03": {
            "1. open": "167.4000",
            "2. high": "168.2200",
            "3. low": "166.2250",
            "4. close": "167.4300",
            "5. volume": "5263342"
            },
            "2024-05-02": {
            "1. open": "167.4000",
            "2. high": "168.2200",
            "3. low": "166.2250",
            "4. close": "165.4300",
            "5. volume": "5263342"
            }
        }
    }

    return data


