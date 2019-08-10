from django.contrib import admin

# Register your models here.

from .models import currency_convertion
from .forms import CurrencyPredictionForm


class Predictionform(admin.ModelAdmin):
    list_display = ["__str__"]
    form = CurrencyPredictionForm


admin.site.register(currency_convertion, Predictionform)
