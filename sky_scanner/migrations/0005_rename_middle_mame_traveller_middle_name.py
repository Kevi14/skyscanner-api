# Generated by Django 4.2.1 on 2023-10-21 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sky_scanner', '0004_rename_first_mame_traveller_first_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveller',
            old_name='middle_mame',
            new_name='middle_name',
        ),
    ]