import uuid
from datetime import datetime, timedelta, timezone
from django.db import models
from django.contrib.auth.models import User, Permission
from apps.core.facilities.models import Facilities


def get_account_expiry(delta=30):
    return datetime.now(timezone.utc) + timedelta(days=delta)


def get_profile_expiry():
    return get_account_expiry(3600)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
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


# The organization creation will be handled by TherapEase staff to properly validate the entity.
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="My Organization")
    members = models.ManyToManyField(User)
    facilities = models.ManyToManyField(Facilities)
    # other metadata will be the contact, address, website, etc.
    other_metadata = models.JSONField(default=dict)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Organizations"
        ordering = ["-create_date"]
        permissions = (
            (
                "manage_organization",
                "Can manage organization",
            ),  # this is the superuser for org scope
            (
                "manage_organization_members",
                "Can manage members to organization",
            ),  # this is the user admin at org scope, can also add owner/members to facilities
            (
                "manage_organization_facilities",
                "Can manage facilities of the organization",
            ),  # super
        )

    def __str__(self):
        return str(self.name)

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    # member management
    def add_member(self, user):
        return self.members.add(user)

    def remove_member(self, user):
        return self.members.remove(user)

    # facility management
    # once a facility is created it is automatically added to the organization
    def add_facility(self, facility):
        return self.facilities.add(facility)


# this will be the list of all roles
class Roles(models.Model):
    ROLE_TYPES = (
        ("org", "Organization"),
        ("family", "Family"),
    )

    name = models.CharField(default="member", max_length=50)
    role_type = models.CharField(default="org", max_length=20, choices=ROLE_TYPES)
    # the permissions here are focused on the management of organization
    # if this is empty default to readonly mode
    permissions = models.ManyToManyField(Permission)

    class Meta:
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name


# Organization Roles can only be configured by TherapEase administrators
class OrganizationRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_org_role"
    )
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="active")
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "OrganizationRoles"
        ordering = ["-create_date"]

    def save(self, *args, **kwargs):
        if self.organization.is_member(self.user):
            super(OrganizationRole, self).save(*args, **kwargs)
        return False
