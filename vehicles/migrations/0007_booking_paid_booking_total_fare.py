# Generated by Django 5.2 on 2025-05-04 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_rename_model_vehicle_model_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='total_fare',
            field=models.FloatField(default=0),
        ),
    ]
