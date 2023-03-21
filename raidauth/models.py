from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)
    is_verified = models.BooleanField(default = False)
    mobile_number = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    user_type = models.CharField(max_length=20, default= 'user')
    city = models.CharField(max_length=20, blank=True, null=True)
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


class DocumentsList(models.Model):
    driver_id = models.ForeignKey(User, on_delete = models.CASCADE)
    aadhar_doc = models.ImageField(upload_to='documents/',blank=True, null=True)
    pancard_doc = models.ImageField(upload_to='documents/',blank=True, null=True)
    voter_doc = models.ImageField(upload_to='documents/',blank=True, null=True)
    license_doc = models.ImageField(upload_to='documents/',blank=True, null=True)
    rc_doc  = models.ImageField(upload_to='documents/',blank=True, null=True)
    insurance_doc = models.ImageField(upload_to='documents/',blank=True, null=True)
    status = models.CharField(max_length=255, default = "open")
    vehicle_type = models.ManyToManyField(VehicleType, blank=True, null=True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    def __str__(self):
        return self.status
    



class RideHistory(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    from_location = models.CharField(max_length = 255)
    to_location = models.CharField(max_length = 255)
    status = models.CharField(max_length = 255, default = "started")
    fare = models.CharField( max_length=50)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    def __str__(self):
        return self.user_id
    