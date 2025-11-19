from django import forms
from .models import RentRecord

class RentRecordForm(forms.ModelForm):
    class Meta:
        model = RentRecord
        fields = '__all__'
