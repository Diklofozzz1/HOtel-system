# Generated by Django 3.2 on 2021-05-27 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0009_auto_20210523_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='positions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='reg.positions'),
        ),
    ]
