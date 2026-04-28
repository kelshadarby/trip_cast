from rest_framework import serializers
from .models import Waypoint

class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = '__all__'

class WaypointResultSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    location_type = serializers.CharField()
    google_place_id = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()