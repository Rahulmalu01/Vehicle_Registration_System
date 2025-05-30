# Generated by Django 5.2 on 2025-05-03 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_remove_vehicle_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
