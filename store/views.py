from django.shortcuts import render, get_object_or_404
from .models import Product, Category 

# Filtering logic for the product from backend 
def store(request, category_slug=None):
    categories = None
    products = None

    # Check if category_slug is provided
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    product_count = products.count()

    context = { 
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)




# this code will
# Define the view function that will display a product's details based on its category and product slugs.
def product_detail(request, category_slug, product_slug):
    try:
        # Attempt to retrieve the product based on the category slug and product slug
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        # If an error occurs (e.g., product not found), raise the exception
        raise e
    
    # Prepare the context dictionary to pass the product data to the template
    context = {
        'single_product': single_product,  # The product retrieved will be passed as 'single_product' to the template
    }
    
    # Render the 'product_detail.html' template with the product data
    return render(request, 'store/product_detail.html', context)
