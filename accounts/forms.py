import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Account,UserProfile
from django.core.validators import RegexValidator


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Password must contain at least one uppercase letter, one number, and one special character."
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account  
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'province', 'city', 'phone_number', 'gender', 'password'
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")


class UserProfileForm(forms.ModelForm):
    address =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing..', 'required': 'required'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-upload-input'}))
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-upload-input'}))
    zipcode = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d+$', message="Zip Code must contain only numbers.")]
    )

    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'state','city','zipcode']

