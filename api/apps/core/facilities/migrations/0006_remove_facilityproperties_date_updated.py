# Generated by Django 4.2.7 on 2023-12-07 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_alter_facilityproperties_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilityproperties',
            name='date_updated',
        ),
    ]