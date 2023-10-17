from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser, Profile


# Autogenerate User Profile
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:

            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            # Create the user profile if not exist
            Profile.objects.create(user=instance)
            print('Profile did not exist, but I created one.')
        print('user is updated')