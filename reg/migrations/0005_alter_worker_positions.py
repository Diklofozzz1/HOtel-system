# Generated by Django 3.2 on 2021-05-05 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0004_alter_worker_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='positions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reg.positions'),
        ),
    ]