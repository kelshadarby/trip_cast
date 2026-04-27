import requests
from django.conf import settings

def get_place_coordinates(google_place_id):
    url="https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "place_id": google_place_id,
        "key": settings.GOOGLE_API_KEY
    }

    response = requests.post(url, params=params)
    return response.json()