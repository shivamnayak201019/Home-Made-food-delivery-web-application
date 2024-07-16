from django import forms
from .models import Customers1

class createform(forms.ModelForm):
    class Meta:
        model=Customers1
        fields=['c_first_name','c_last_name','c_phone_number','c_passward','c_email']