# Generated by Django 4.2.1 on 2023-10-21 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sky_scanner', '0018_remove_bookedsegment_tax_percentage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Referral',
        ),
    ]