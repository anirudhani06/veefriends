from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Profile


# When any user register or created immediately create a profile table for that user.
@receiver(post_save,sender=User)
def create_user(sender,instance,created,*args, **kwargs):
    profile = Profile()
    user = instance
    if created:
        profile.user = user
        profile.username = user.username
        profile.name = user.name
        profile.email = user.email
        profile.save()
        

# When the profile is updated that time the user column also updated.
@receiver(post_save,sender=Profile)
def update_user(sender,instance,created,*args, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.username = profile.username
        user.name = profile.name
        user.email = profile.email
        user.save()