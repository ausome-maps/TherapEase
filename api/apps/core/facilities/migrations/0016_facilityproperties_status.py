# Generated by Django 4.2.7 on 2023-12-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0015_alter_facilities_geometry'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityproperties',
            name='status',
            field=models.CharField(default='active', max_length=10),
        ),
    ]
