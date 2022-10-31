from .models import *
from django import forms

class CreateCashoutForm(forms.ModelForm):
    class Meta:
        model = Cashout
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(CreateCashoutForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
    
class EditCashoutForm(forms.ModelForm):

    approved = forms.BooleanField() 
    class Meta:
        model = Cashout
        fields = ['approved']

    def __init__(self, *args, **kwargs):
        super(EditCashoutForm, self).__init__(*args, **kwargs)
        self.fields['approved'].widget.attrs.update({'class': 'form-check-input'})