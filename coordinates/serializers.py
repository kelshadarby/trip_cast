from rest_framework import serializers
from .models import CoordinateSet

class CoordinateSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinateSet
        fields = '__all__'
        