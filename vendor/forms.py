from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-upload-input'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']