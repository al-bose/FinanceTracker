from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    UTILITIES = 'Utilities'
    FOOD = 'Food'
    HOUSING = 'Housing'
    TRANSPORTATION = 'Transportation'
    CLOTHING = 'Clothing'
    ENTERTAINMENT = 'Entertainment'
    MISC = "Miscellaneous"

    TYPE_CHOICES = {
        UTILITIES : 'Utilities',
        FOOD : 'Food',
        HOUSING : 'Housing',
        TRANSPORTATION : 'Transportation',
        CLOTHING : 'Clothing',
        ENTERTAINMENT : 'Entertainment',
        MISC : "Miscellaneous"
    }

    type = models.CharField(
        max_length = 32,
        choices = TYPE_CHOICES,
        default = MISC
    )
    