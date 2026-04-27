from django.db import models
from route_planner.models import Trip

class RestStop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    google_place_id = models.CharField(max_length=255)
    location_type = models.CharField(max_length=225, blank=True)
    address = models.CharField(max_length=225)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name