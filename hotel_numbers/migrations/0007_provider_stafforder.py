# Generated by Django 3.2 on 2021-05-27 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel_numbers', '0006_storage_dirty_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=15, null=True)),
                ('phone_number', models.CharField(default='', max_length=20, unique='True')),
            ],
        ),
        migrations.CreateModel(
            name='StaffOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, null=True)),
                ('coast', models.FloatField(null=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('count', models.IntegerField(default=0)),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel_numbers.provider')),
                ('stuff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel_numbers.storage')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]