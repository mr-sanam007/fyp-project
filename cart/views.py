from django.shortcuts import render,redirect, get_object_or_404
from store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

   
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    elif request.method == 'GET':
        variation_ids = request.GET.get('variations')
        if variation_ids:
            variation_ids = variation_ids.split(',')
            for var_id in variation_ids:
                try:
                    variation = Variation.objects.get(id=var_id)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    # Check if cart item with same product and variations exists
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    existing_cart_item = None

    for item in cart_items:
        item_variations = list(item.variations.all())
        if sorted(item_variations, key=lambda x: x.id) == sorted(product_variation, key=lambda x: x.id):
            existing_cart_item = item
            break

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation) > 0:
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()

    return redirect('cart')

#  logic for removing cart and able to decrement the quantity by 1
from django.shortcuts import get_object_or_404

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    variation_ids = request.GET.get('variations')
    if variation_ids:
        variation_ids = variation_ids.split(',')
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        cart_item = None
        for item in cart_items:
            item_variation_ids = list(item.variations.values_list('id', flat=True))
            if sorted(item_variation_ids) == sorted([int(v) for v in variation_ids]):
                cart_item = item
                break
    else:
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    variation_ids = request.GET.get('variations')
    if variation_ids:
        variation_ids = variation_ids.split(',')
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        cart_item = None
        for item in cart_items:
            item_variation_ids = list(item.variations.values_list('id', flat=True))
            if sorted(item_variation_ids) == sorted([int(v) for v in variation_ids]):
                cart_item = item
                break
    else:
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()

    if cart_item:
        cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    # Initialize all variables with default values
    shipping_charge = 0
    grand_total = 0
    cart_items = []  # Initialize as empty list instead of None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            cart_item.item_total = cart_item.product.price * cart_item.quantity
            total += cart_item.item_total
            quantity += cart_item.quantity
            # Add variation_ids_str attribute
            variation_ids = cart_item.variations.values_list('id', flat=True)
            cart_item.variation_ids_str = ",".join(str(id) for id in variation_ids)
        
        shipping_charge = (2 * total)/100
        grand_total = total + shipping_charge
        
    except ObjectDoesNotExist:
        # All variables already have their default values
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

def checkout(request, total=0, quantity=0, cart_items=None):
    shipping_charge = 0
    grand_total = 0
    tax = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            cart_item.item_total = cart_item.product.price * cart_item.quantity
            total += cart_item.item_total
            quantity += cart_item.quantity

        shipping_charge = (2 * total) / 100
        tax = (13 * total) / 100
        grand_total = total + shipping_charge + tax

    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        # For now, just redirect to cart or a placeholder page after form submission
        return redirect('cart')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_charge': shipping_charge,
        'tax': tax,
        'grand_total': grand_total,
        'currency_symbol': '₹',  # Assuming Indian Rupee, adjust as needed
    }
    return render(request, 'store/checkout.html', context)

