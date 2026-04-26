from django.db import models

class Trip(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    polyline = models.TextField(blank=True, null=True)
    total_distance_meters = models.IntegerField(blank=True, null=True)
    total_duration_seconds = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} to {self.destination}"
    

class Waypoint(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='waypoints')
    lat = models.FloatField()
    lng = models.FloatField()
    order = models.IntegerField()

    def __str__(self):
        return f"Waypoint {self.order} for {self.trip}"