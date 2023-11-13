import uuid
from datetime import datetime, timedelta, timezone
from django.db import models
from django.contrib.auth.models import User


def get_account_expiry(delta=30):
    return datetime.now(timezone.utc) + timedelta(days=delta)


def get_profile_expiry():
    return get_account_expiry(3600)


class Profile(models.Model):
    """
    expand this table to add more info for the user like address, job, role, etc.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=999, default="My Organization")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    login_count = models.IntegerField(default=0)
    account_expiry = models.DateTimeField(default=get_profile_expiry, editable=True)

    class Meta:
        verbose_name_plural = "Profiles"
        ordering = ["-create_date"]

    def __str__(self):
        return str(self.user.email)

    def add_login_count(self):
        self.login_count += 1
