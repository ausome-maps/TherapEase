# Generated by Django 4.2.7 on 2023-12-19 09:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facilities", "0012_alter_facilities_geometry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facilityproperties",
            name="images",
            field=models.JSONField(blank=True, default=[], null=True),
        ),
    ]
