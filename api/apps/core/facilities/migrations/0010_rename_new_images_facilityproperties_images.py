# Generated by Django 4.2.7 on 2023-12-16 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0009_rename_images_facilityproperties_old_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facilityproperties',
            old_name='new_images',
            new_name='images',
        ),
    ]
