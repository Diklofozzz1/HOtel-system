# Generated by Django 3.2 on 2021-05-14 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_order_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='executed',
            field=models.BooleanField(default=False),
        ),
    ]