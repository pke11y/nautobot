# Generated by Django 3.1.3 on 2021-02-02 03:58

import dcim.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtualization', '0019_standardize_name_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vminterface',
            name='mac_address',
            field=dcim.fields.MACAddressCharField(blank=True, null=True),
        ),
    ]
