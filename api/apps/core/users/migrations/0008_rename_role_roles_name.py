# Generated by Django 4.2.7 on 2023-12-23 07:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_remove_organizationrole_permission_roles_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="roles",
            old_name="role",
            new_name="name",
        ),
    ]
