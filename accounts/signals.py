from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Account, UserProfile
   
@receiver(post_save, sender= Account)  #decorater to send signal when user is created
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print('created')
    if created: 
        UserProfile.objects.create(user=instance)
        print(' userprofile created successfully')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the userprofile if it not exist
            UserProfile.objects.create(user=instance)
           


@receiver(pre_save, sender=Account)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass