from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Facilities, FacilityProperties


@receiver(post_save, sender=FacilityProperties)
def add_moderator_permission_to_subscription_owner(
    sender, instance=None, created=False, **kwargs
):
    if created:
        Facilities.objects.create(id=instance.osm_id, properties=instance)
