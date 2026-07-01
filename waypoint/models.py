from django.db import models

class Waypoint(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=225)
    location_type = models.CharField(max_length=225, blank=True)
    google_place_id = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name