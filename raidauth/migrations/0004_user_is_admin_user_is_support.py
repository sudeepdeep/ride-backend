# Generated by Django 4.1.7 on 2023-03-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raidauth', '0003_remove_user_is_driver_remove_user_is_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_support',
            field=models.BooleanField(default=False),
        ),
    ]
