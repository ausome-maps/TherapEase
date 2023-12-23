# Generated by Django 4.2.7 on 2023-12-23 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0011_rename_permission_roles_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationrole",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_org_role",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
