# Generated by Django 3.2 on 2021-05-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_numbers', '0004_auto_20210527_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='dirty_staff',
        ),
        migrations.AddField(
            model_name='dirtylineal',
            name='dirty_staff',
            field=models.IntegerField(default=0),
        ),
    ]
