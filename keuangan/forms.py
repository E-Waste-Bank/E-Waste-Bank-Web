from .models import *
from django import forms

class CreateCashoutForm(forms.ModelForm):
    class Meta:
        model = Cashout
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(CreateCashoutForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 0.0
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
    
class EditCashoutForm(forms.Form):

    approved = forms.BooleanField(widget=forms.CheckboxInput, required= False)

    def __init__(self, *args, **kwargs):
        super(EditCashoutForm, self).__init__(*args, **kwargs)
        self.fields['approved'].widget.attrs.update({'class': 'form-check-input'})

class EditUangUserForm(forms.Form):

    uang_user = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(EditUangUserForm, self).__init__(*args, **kwargs)
        self.fields['uang_user'].widget.attrs['min'] = 0.0
        self.fields['uang_user'].widget.attrs.update({'class': 'form-control'})