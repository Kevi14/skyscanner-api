# Generated by Django 4.2.1 on 2023-10-21 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_type', models.CharField(choices=[(1, 'customer'), (2, 'provider')], default='customer', max_length=20)),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('frequent_flyer_number', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
