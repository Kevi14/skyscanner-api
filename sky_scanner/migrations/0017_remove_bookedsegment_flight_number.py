# Generated by Django 4.2.1 on 2023-10-21 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sky_scanner', '0016_ticket_booked_segments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookedsegment',
            name='flight_number',
        ),
    ]
