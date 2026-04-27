import requests
from django.conf import settings

def get_rest_stop(textQuery, polyline):
    url="https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.primaryType,places.types"
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