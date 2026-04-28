import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from route.services import get_route
from .models import Route

def get_rest_stop(textQuery, polyline):
    url="https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.primaryTypeDisplayName"
    }

    body = {
        "textQuery": textQuery,
        "searchAlongRouteParameters": {
            "polyline": {
                "encodedPolyline": polyline
            }
        }
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()

def get_place_coordinates(google_place_id):
    url="https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "place_id": google_place_id,
        "key": settings.GOOGLE_API_KEY
    }

    response = requests.post(url, params=params)
    return response.json()

def update_trip_with_intermediates(trip_id, latitude, longitude):
    trip = get_object_or_404(Route, id=trip_id)
    if intermediate not in trip.intermediates:
        trip.intermediates = trip.intermediates + [
            {"latLng":{
                "latitude": latitude,
                "longitude": longitude
            }}
        ]
        trip.save()
    print(trip.intermediates)
    updated_route = get_route(trip.origin, trip.destination, trip.intermediates)
    return updated_route