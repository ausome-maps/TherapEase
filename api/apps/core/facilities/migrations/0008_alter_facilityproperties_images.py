import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_alter_facilityproperties_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityproperties',
            name='new_images',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]
