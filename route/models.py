from django.db import models
from waypoint.models import Waypoint

class Route(models.Model):
    origin = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name='origin')
    destination = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name='destination')
    polyline = models.TextField(blank=True, null=True)
    total_distance_meters = models.IntegerField(blank=True, null=True)
    total_duration_seconds = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class RouteWaypoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE)
    waypoint_position = models.IntegerField()