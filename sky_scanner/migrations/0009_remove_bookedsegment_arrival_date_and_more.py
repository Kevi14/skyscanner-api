# Generated by Django 4.2.1 on 2023-10-21 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sky_scanner', '0008_alter_flight_arrival_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookedsegment',
            name='arrival_date',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='arrival_date',
        ),
    ]
