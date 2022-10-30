from .models import *
from django import forms

class CreateCashoutForm(forms.ModelForm):
    class Meta:
        model = Cashout
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(CreateCashoutForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})