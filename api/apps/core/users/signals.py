from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .models import Profile
from .tasks import send_registration_email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)
        group, created = Group.objects.get_or_create(name=instance.email)
        group.user_set.add(instance)
        # send_registration_email.delay(
        #     instance.first_name, profile.account_expiry, instance.email
        # )
