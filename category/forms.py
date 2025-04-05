from django import forms
from .models import Category
from  store.models import Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['Category_name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'image', 'stock', 'category', 'is_available']
