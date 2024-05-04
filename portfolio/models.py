from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Positions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=10, decimal_places=5)
    cost_basis = models.DecimalField(max_digits=10, decimal_places=5)

    RETIREMENT = "401K"
    ROTH = "ROTH"
    INDIVIDUAL = "INDIVIDUAL"
    CRYPTO = "CRYPTO"

    TYPE_CHOICES = {
        RETIREMENT : "401K",
        ROTH: "Roth IRA",
        INDIVIDUAL: "Individual",
        CRYPTO: "Cryptocurrency"
    }

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=INDIVIDUAL
    )