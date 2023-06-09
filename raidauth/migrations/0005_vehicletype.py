# Generated by Django 4.1.7 on 2023-03-13 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raidauth', '0004_user_is_admin_user_is_support'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=100)),
                ('cost_per_km', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('vehicle_image', models.ImageField(upload_to='vehicle-images')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
