from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import UserForm
from .models import Account, UserProfile
from vendor.forms import VendorForm
from .utils import detectUser
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required,user_passes_test
from vendor.models import Vendor
from  accounts.utils import send_verfication_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# restricting the user from accesing the unauthorize pages
def check_role_SELLER(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
    
def check_role_CUSTOMER(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied
    
# userregistration logic
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

            # send verification email
            mail_subject = "please activate your account"
            email_template = "accounts/emails/account_verification.html"
            send_verfication_email(request, account,mail_subject,email_template)
            messages.success(request, 'Account created successfully!')
            return redirect('registerUser')
        else:
            print("Form errors:", form.errors)  # Check console for validation errors
    else:
        form = UserForm()

    return render(request, 'accounts/registerUser.html', {'form': form})



def activate(request , uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is now active!')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    


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
            # send verification email
            mail_subject = "please activate your account"
            email_template = "accounts/emails/account_verification.html"
            send_verfication_email( request, user,mail_subject,email_template)

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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        if request.user.is_admin or request.user.is_superadmin:
            return redirect('/admin/')  # Django admin panel
        elif request.user.role == Account.SELLER:
            return redirect('vendorDashboard')
        else:
            return redirect('customerDashboard')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            
            if user.is_admin or user.is_superadmin:
                return redirect('/admin/')  # Django admin panel
            elif user.role == Account.SELLER:
                return redirect('vendorDashboard')
            else:
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
@login_required(login_url ='login')
@user_passes_test(check_role_CUSTOMER)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_SELLER)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    context = {
        'vendor': vendor,
    
    }
    return render(request, 'accounts/vendorDashboard.html', context)

# myAccount
@login_required(login_url ='login')
def myAccount(request):
    user = request.user
    redirectURl =detectUser(user)
    return render(request, 'accounts/login.html')


# forget password

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if  Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact= email)

            # send reset password email
            mail_subject ='Reset Your Password'
            email_template = 'accounts/email/reset_password_email.html'
            send_verfication_email(request, user,mail_subject, email_template)
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('myAccount')
        else:
            messages.error(request, 'Email does not exist')
            return redirect('forgot_password')
        
    return render(request, 'accounts/forgot_password.html')


# reset password


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            pk = request.session.get('uid')
            user =Account.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password and confirm password does not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


# reset password validation 

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.info(request,'please reset your password')
        return redirect('reset_password')
    
    else:
        messages.error(request, 'this link has expired')
        return redirect('myAccount')

