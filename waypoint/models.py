from django.db import models

class Waypoint(models.Model):

    WAYPOINT_TYPE_CHOICES = [
        ('origin', 'Origin'),
        ('destination', 'Destination'),
        ('intermediate', 'Intermediate'),
    ]
        
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=225)
    location_type = models.CharField(max_length=225, blank=True)
    google_place_id = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    waypoint_type = models.CharField(
        max_length=20,
        choices=WAYPOINT_TYPE_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name