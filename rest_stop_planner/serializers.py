from rest_framework import serializers
from .models import RestStop

class RestStopResultSerializer(serializers.Serializer):
    google_place_id = serializers.CharField()
    name = serializers.CharField()
    location_type = serializers.CharField()
    address = serializers.CharField()

class RestStopSerializer(serializers.Serializer):
    class Meta:
        model = RestStop
        fields = '__all__'

    def create(self, validated_data):
        return RestStop.objects.create(**validated_data)