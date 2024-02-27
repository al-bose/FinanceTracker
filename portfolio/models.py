from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Positions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_date = models.DateTimeField()
    ticker = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=10, decimal_places=5)
    cost_basis = models.DecimalField(max_digits=10, decimal_places=5)