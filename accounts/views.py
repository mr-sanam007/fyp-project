from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import UserForm
from .models import Account, UserProfile
from vendor.forms import VendorForm
from .utils import detectUser

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Extract ALL fields from the form (including phone_number)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']  

            # Include phone_number in create_user() if your model requires it
            account = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                phone_number=phone_number  # ADD THIS
            )
            account.role = Account.CUSTOMER
            account.save()

            messages.success(request, 'Account created successfully!')
            return redirect('registerUser')
        else:
            print("Form errors:", form.errors)  # Check console for validation errors
    else:
        form = UserForm()

    return render(request, 'accounts/registerUser.html', {'form': form})


def vendorsignup(request):
    # Redirect if user is already logged in
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number'] 
            
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                phone_number=phone_number  
            )
            user.role = user.SELLER
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            messages.success(request, 'Your account has been created successfully! Please wait for approval.')
            return redirect('vendorsignup')
        else:
            print("Invalid form")
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/vendor_signup.html', context)

# login logic goes here 
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in!')
        return redirect('vendorDashboard')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success( request, 'You have been logged in successfully!')
            return redirect('customerDashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'accounts/login.html')
        
   
  

# Logout
def logout(request):
    auth.logout(request)
    messages.info(request, 'You have logged out successfully')
    return redirect('login')

# Dashboard
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')


def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')


# myAccount

def myAccount(request):
    user = request.user
    redirectURl =detectUser(user)
    return render(request, 'accounts/myAccount.html')
