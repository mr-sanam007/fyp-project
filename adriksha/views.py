from django.shortcuts import render
from store.models import Product 
from vendor.models import Vendor
def home(request):
    products = Product.objects.all().filter(is_available=True)
    vendor =Vendor.objects.filter(is_approved=True, user__is_active = True)
    context = { 
        'products': products,
        'vendor': vendor
    }
    return render(request, 'home.html', context)
