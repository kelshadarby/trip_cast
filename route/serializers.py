from rest_framework import serializers
from .models import Route, RouteWaypoint

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class RouteWaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteWaypoint
        fields = '__all__'
