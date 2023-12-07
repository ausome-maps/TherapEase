# Generated by Django 4.2.7 on 2023-12-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_remove_facilityproperties_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityproperties',
            name='address',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='alt_contact_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='contact_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='email_address',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='info_src_designation',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='info_src_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='landmarks_desc',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='placename',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='region',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilityproperties',
            name='website',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
