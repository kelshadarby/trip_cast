from django.db import models
from rest_stop_planner.models import RestStop

class CoordinateSet(models.Model):
    rest_stop = models.ForeignKey(RestStop, on_delete=models.CASCADE, related_name='rest_stop')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"
