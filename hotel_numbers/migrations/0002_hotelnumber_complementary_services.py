# Generated by Django 3.2 on 2021-05-10 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_numbers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelnumber',
            name='complementary_services',
            field=models.CharField(default='', max_length=50),
        ),
    ]
