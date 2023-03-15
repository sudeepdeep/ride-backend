# Generated by Django 4.1.7 on 2023-03-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raidauth', '0002_user_username_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_driver',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_user',
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(default='user', max_length=20),
        ),
    ]