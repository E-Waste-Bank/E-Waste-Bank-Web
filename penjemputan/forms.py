from django import forms
from .models import Penjemputan

class CreatePenjemputanForm(forms.ModelForm):
    class Meta:
        model = Penjemputan
        fields = [
            'tanggal_jemput', 
            'waktu_jemput',
            'jenis_sampah',
            'berat_sampah',
            'alamat',
            ]
        widgets = {
            'tanggal_jemput': forms.TextInput(attrs={'type': 'date'}),
            'waktu_jemput': forms.TimeInput(attrs={'type': 'time'}),
            'alamat': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super(CreatePenjemputanForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'