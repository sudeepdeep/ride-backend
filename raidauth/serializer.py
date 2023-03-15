from rest_framework import serializers
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.EmailField()
    otp = serializers.CharField()


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'
    # vehicle_name = serializers.CharField()
    # cost_per_km = serializers.IntegerField()
    # status = serializers.BooleanField()
    # vehicle_image = serializers.ImageField()