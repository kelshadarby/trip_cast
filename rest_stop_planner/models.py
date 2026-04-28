from django.db import models
from route.models import Route

class RestStop(models.Model):
    trip = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    google_place_id = models.CharField(max_length=255)
    location_type = models.CharField(max_length=225, blank=True)
    address = models.CharField(max_length=225)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    
class RouteWaypoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route')
    latitude = models.FloatField()
    longitude = models.FloatField()