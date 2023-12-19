# Generated by Django 4.2.7 on 2023-12-19 09:28

import apps.core.facilities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0014_alter_facilityproperties_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilities',
            name='geometry',
            field=models.JSONField(blank=True, default=apps.core.facilities.models.default_coordinates, null=True),
        ),
    ]