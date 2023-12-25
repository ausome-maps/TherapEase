# Generated by Django 4.2.7 on 2023-12-23 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0006_organizationrole_alter_organization_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organizationrole",
            name="permission",
        ),
        migrations.CreateModel(
            name="Roles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(default="member", max_length=50)),
                ("role_types", models.CharField(default="org", max_length=20)),
                ("permission", models.ManyToManyField(to="auth.permission")),
            ],
            options={
                "verbose_name_plural": "Roles",
            },
        ),
        migrations.AlterField(
            model_name="organizationrole",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.roles"
            ),
        ),
    ]