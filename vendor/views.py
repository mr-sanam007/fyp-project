
from django.shortcuts import render, get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from store.models import Product
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_SELLER
from category.models import Category
from category.forms import CategoryForm,ProductForm

from django.template.defaultfilters import slugify
# helper function to get if user is a seller
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor
# Create your views here.
@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES,instance = profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'setting change successfully')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form =UserProfileForm( instance= profile)
        vendor_form = VendorForm(instance= vendor)

    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor,
        }
    return render(request, 'vendor/vprofile.html',context)

@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(Vendor=vendor).order_by('created_at')
    context = {
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def products_by_category(request, pk=None):
    vendor   = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(vendor=vendor, category=category)  # Fixed: products.objects → Product.objects
    print(products)
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'vendor/products_by_category.html', {'products': products, 'category': category})

# crud category
@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['Category_name']
            category = form.save(commit=False)
            category.Vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('menu_builder')
        else:
            messages.error(request, 'category already exist ')

    else:
        form = CategoryForm()
    form = CategoryForm()
    context = {
        'form': form
    }

    return render(request, 'vendor/add_category.html', context)


# edit category
@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.Vendor = get_vendor(request)
            category.slug = slugify(form.cleaned_data['Category_name'])  # Note the capital C
            category.save()
            messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)

# delete category
@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_SELLER)
def add_product(request, pk=None):
    vendor = get_vendor(request)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            productname = form.cleaned_data['product_name']
            product = form.save(commit=False)
            product.vendor = vendor  # This is for the Product model
            product.slug = slugify(productname)
            product.save()
            messages.success(request, 'Product added successfully')
            return redirect('products_by_category', product.category.id)
        else:
            print(form.errors)
    else:
        form = ProductForm()
        # Filter categories by the Vendor field (capital V)
        form.fields['category'].queryset = Category.objects.filter(Vendor=vendor)
    
    context = {
        'form': form,
        'vendor': vendor,
    }
    return render(request, 'vendor/add_product.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_SELLER)
def edit_product(request, pk):
    vendor = get_vendor(request)
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.slug = slugify(form.cleaned_data['product_name'])
            product.save() 
            messages.success(request, 'Product updated successfully')
            return redirect('products_by_category', product.category.id)
        else:
            print(form.errors)  # Debugging: print form errors in the console
            messages.error(request, 'Please correct the errors below')
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(Vendor=vendor)
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'vendor/edit_product.html', context)


# delete product
@login_required(login_url ='login')
@user_passes_test(check_role_SELLER)
def delete_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'product deleted successfully')
    return redirect('products_by_category',product.category.id)
