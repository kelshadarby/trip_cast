from rest_framework import serializers
from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    waypoints = WaypointSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'