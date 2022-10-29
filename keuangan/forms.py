from .models import *
from django import forms

class CreateCashoutForm(forms.Form):
    amount = forms.FloatField(required=True, min_value=0)