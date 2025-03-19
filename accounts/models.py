from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import OneToOneField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError(' user should have email address')
        
        if not username:
            raise ValueError(" user should have username")
        
        user = self.model(
            email =self.normalize_email(email),
            username =username,
            first_name = first_name,
            last_name = last_name,

        )

        user. set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser( self, first_name, last_name, email, username, password):
        user = self.create_user(
            email =self.normalize_email(email),
            username =username,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user

    # custom user model here

class Account(AbstractBaseUser):
    STORE =1
    CUSTOMER =2
    ROLE_CHOICE =(
        (STORE, 'STORE'),
        (CUSTOMER,'CUSTOMER'),
    )
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank= True, null= True)

    # optional field
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superadmin = models.BooleanField(default=False)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects =MyAccountManager()

    def __str__(self):  
        return self.email

    def has_perm(self, perm, obj=None):  
        return self.is_admin

    def has_module_perms(self, app_label):  
        return True 
    

# user profile model

class UserProfile(models.Model):
    user = OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo =  models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    state =   models.CharField(max_length=25, blank=True, null=True)
    city =    models.CharField(max_length=25, blank=True, null=True)
    zipcode = models.CharField(max_length=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
@receiver(post_save, sender= Account)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print('created')
    if created: 
        UserProfile.objects.create(user=instance)
        print(' userprofile created successfully')
    else:
        profile= UserProfile.objects.get(user=instance)
        print("user profile successfully updated")
