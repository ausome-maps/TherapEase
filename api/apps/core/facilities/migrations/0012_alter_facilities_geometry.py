# Generated by Django 4.2.7 on 2023-12-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0011_remove_facilityproperties_old_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilities',
            name='geometry',
            field=models.JSONField(blank=True, default={'coordinates': [0, 0], 'type': 'Point'}, null=True),
        ),
    ]