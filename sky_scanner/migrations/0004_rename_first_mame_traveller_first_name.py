# Generated by Django 4.2.1 on 2023-10-21 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sky_scanner', '0003_iatacode_airport_name_iatacode_city_flight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveller',
            old_name='first_mame',
            new_name='first_name',
        ),
    ]
