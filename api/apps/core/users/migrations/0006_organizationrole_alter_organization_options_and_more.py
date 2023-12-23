# Generated by Django 4.2.7 on 2023-12-23 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("facilities", "0015_alter_facilities_geometry"),
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0005_organization_organizationroles"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizationRole",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("role", models.CharField(default="member", max_length=50)),
                ("create_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "OrganizationRoles",
                "ordering": ["-create_date"],
            },
        ),
        migrations.AlterModelOptions(
            name="organization",
            options={
                "ordering": ["-create_date"],
                "permissions": (
                    ("manage_organization", "Can manage organization"),
                    (
                        "manage_organization_members",
                        "Can manage members to organization",
                    ),
                    (
                        "manage_organization_facilities",
                        "Can manage facilities of the organization",
                    ),
                ),
                "verbose_name_plural": "Organizations",
            },
        ),
        migrations.RemoveField(
            model_name="profile",
            name="organization",
        ),
        migrations.AddField(
            model_name="organization",
            name="facilities",
            field=models.ManyToManyField(to="facilities.facilities"),
        ),
        migrations.AddField(
            model_name="organization",
            name="name",
            field=models.CharField(default="My Organization", max_length=100),
        ),
        migrations.AddField(
            model_name="organization",
            name="other_metadata",
            field=models.JSONField(default=dict),
        ),
        migrations.DeleteModel(
            name="OrganizationRoles",
        ),
        migrations.AddField(
            model_name="organizationrole",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.organization"
            ),
        ),
        migrations.AddField(
            model_name="organizationrole",
            name="permission",
            field=models.ManyToManyField(to="auth.permission"),
        ),
        migrations.AddField(
            model_name="organizationrole",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
