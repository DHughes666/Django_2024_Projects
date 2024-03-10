from rest_framework import serializers
from .models import Inmate, Staff

class InmateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inmate
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'