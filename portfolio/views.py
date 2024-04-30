from django.shortcuts import render
from django.http import HttpResponse
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

# Create your views here.

@login_required
def main(request):
    stocks = Positions.objects.filter(user_id=request.user.id)

    #calculate total current value for stock
    total_ticker_prices = {}

    total_prices = {
        "current_value": 0,
        "total_cost": 0,
        "percentage_change": 0
    }

    for stock in stocks:
        ticker = stock.ticker

        env = environ.Env()
        environ.Env.read_env()

        response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey='+env("API_KEY"))
        #data = response.json()

        data = {
            "Meta Data": {
                "1. Information": "Daily Prices (open, high, low, close) and Volumes",
                "2. Symbol": "TSLA",
                "3. Last Refreshed": "2024-04-29",
                "4. Output Size": "Compact",
                "5. Time Zone": "US/Eastern"
            },
            "Time Series (Daily)": {
                "2024-04-29": {
                "1. open": "167.4000",
                "2. high": "168.2200",
                "3. low": "166.2250",
                "4. close": "167.4300",
                "5. volume": "5263342"
                }
            }
        }

        most_recent_entry = {}
        if datetime.datetime.now().strftime("%Y-%m-%d") in data["Time Series (Daily)"]:
            most_recent_entry =  data["Time Series (Daily)"][datetime.datetime.now().strftime("%Y-%m-%d")]
        else:
            delta = Timedelta(days=-1)
            most_recent_entry = data["Time Series (Daily)"][(datetime.datetime.now() + delta).strftime("%Y-%m-%d")]

        most_recent_price = Decimal(most_recent_entry["4. close"])

        current_value = most_recent_price * stock.quantity
        total_cost = stock.quantity * stock.cost_basis
        percentage_change = (current_value - total_cost)/total_cost * 100

        total_ticker_prices[stock.ticker] = {
            "current_value": round(current_value,2),
            "total_cost": round(total_cost,2),
            "percentage_change": percentage_change
        }

        total_prices["current_value"] += current_value
        total_prices["total_cost"] += total_cost

        stock.cost_basis = round(stock.cost_basis)

        
    total_prices["percentage_change"] = round(total_prices["current_value"] - total_prices["total_cost"])/total_prices["total_cost"] * 100
    total_prices["current_value"] = round(total_prices["current_value"],2)
    total_prices["total_cost"] = round(total_prices["total_cost"],2)
    context = {"stocks" : stocks, "total_ticker_prices": total_ticker_prices, "total_prices": total_prices}
    return render(request, "portfolio/index.html", context)

@login_required
def createPosition(request):
    if request.method == "POST":
        position = Positions(purchased_date= request.POST["date"], ticker= request.POST["ticker"], quantity= request.POST["quantity"], cost_basis= request.POST["costBasis"])
        position.user = request.user
        position.save()
        return main(request)
    else:
        env = environ.Env()
        environ.Env.read_env()   
        context = {
            "api_key" : env("API_KEY")
        }
        return render(request, "portfolio/createposition.html", context)


