import requests
from django.conf import settings

def find_waypoints(text_query):
    url="https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.primaryTypeDisplayName,places.location"
    }

    body = {
        "textQuery": text_query
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()