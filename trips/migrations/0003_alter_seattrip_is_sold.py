# Generated by Django 4.2.5 on 2023-10-15 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_trip_arrival_time_trip_availabe_tickets_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seattrip',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]