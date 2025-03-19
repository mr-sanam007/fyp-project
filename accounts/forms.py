from django import forms
from .models import Account



class UserForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Account
        fields = [
            'first_name','last_name','username','email','province','city','password','phone_number'
        ]
