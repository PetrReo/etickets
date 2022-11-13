# Generated by Django 2.1.5 on 2022-11-13 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20221113_0602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='featured',
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='event',
            name='ticket_seat_nr',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='ticket_stand_nr',
            field=models.IntegerField(default=20),
        ),
    ]
