# Generated by Django 4.2.1 on 2023-10-21 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sky_scanner.models.booking_data


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sky_scanner', '0006_flight_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_referred', models.DateTimeField(auto_now_add=True)),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to=settings.AUTH_USER_MODEL)),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals_made', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('referrer', 'referred')},
            },
        ),
    ]
