# Generated by Django 4.2.5 on 2023-10-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_alter_bus_total_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='total_seats',
            field=models.IntegerField(choices=[(53, 53)]),
        ),
    ]
