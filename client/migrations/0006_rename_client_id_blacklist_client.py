# Generated by Django 3.2 on 2021-05-16 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_blacklist_case_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blacklist',
            old_name='client_ID',
            new_name='client',
        ),
    ]
