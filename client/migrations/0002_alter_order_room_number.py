# Generated by Django 3.2 on 2021-05-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='room_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
