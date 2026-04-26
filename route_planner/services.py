import requests
from django.conf import settings

def get_route(origin, destination):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }

    body = {
        "origin": {
            "address": origin
        },
        "destination": {
            "address": destination
        },
        "travelMode": "DRIVE"
    }

    response = requests.post(url, json=body, headers=headers)
    print("STATUS CODE:", response.status_code)
    print("GOOGLE RESPONSE:", response.json())
    return response.json()