from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)
    is_verified = models.BooleanField(default = False)
    mobile_number = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    user_type = models.CharField(max_length=20, default= 'user')

    is_support = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS  = []

    def name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.email


class VehicleType(models.Model):
    vehicle_name = models.CharField(max_length=100)
    cost_per_km = models.IntegerField()
    status = models.BooleanField(default = False)
    vehicle_image = models.ImageField(upload_to='images/')
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)


    def __str__(self):
        return self.vehicle_name
