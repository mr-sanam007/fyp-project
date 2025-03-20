from django.shortcuts import render, get_object_or_404
from .models import Product, Category 
from cart.views import _cart_id, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Filtering logic for the product from backend 
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
        paged_products = products  # No pagination inside category view (optional: add if needed)
    else:
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products, 8)  
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = { 
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)



# Define the view function that will display a product's details based on its category and product slugs.
def product_detail(request, category_slug, product_slug):
    # Attempt to retrieve the product based on the category slug and product slug
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    
    # Check if the product is in the cart
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    
    # Prepare the context dictionary to pass the product data to the template
    context = {
        'single_product': single_product,  # The product retrieved will be passed as 'single_product' to the template
        'in_cart': in_cart,  # The in_cart variable will be passed as 'in_cart' to the template
    }
    
    # Render the 'product_detail.html' template with the product data
    return render(request, 'store/product_detail.html', context)