from django.shortcuts import render, get_object_or_404
from .models import Product, Category 
from cart.views import _cart_id, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


# Filtering logic for the product from backend 
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 6)  # Change to a more realistic number like 2 or 3
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products, 6)  # Default pagination for all products
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
    context = {
        'single_product': single_product,  # The product retrieved will be passed as 'single_product' to the template
        'in_cart': in_cart,  # The in_cart variable will be passed as 'in_cart' to the template
    }
    return render(request, 'store/product_detail.html', context)


# logic for search 

def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains= keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


