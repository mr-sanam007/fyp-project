from django.shortcuts import render,redirect, get_object_or_404
from store.models import Product
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
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using cart_id present in session
    except Cart.DoesNotExist:  # Fix is here
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # Probably you meant to increment here?
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
            
        )
        cart_item.save()
    return redirect('cart')

#  logic for removing cart and able to decrement the quantity by 1
from django.shortcuts import get_object_or_404

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Fix: Capitalize Product model
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    # Remove the cart item completely
    cart_item.delete()
    
    return redirect('cart')

# --------------------------------------------------------#
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            cart_item.item_total = cart_item.product.price * cart_item.quantity  # add this line
            total += cart_item.item_total
            quantity += cart_item.quantity
        shipping_charge =(2 * total)/100
        grand_total = total + shipping_charge
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
