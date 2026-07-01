import requests
from django.conf import settings

def fetch_route(origin_google_place_id, destination_google_place_id):
    url="https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
    }

    body = {
        "origin": {
            "placeId": origin_google_place_id
        },
        "destination": {
            "placeId": destination_google_place_id
        },
        "travelMode": "DRIVE"
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()

def fetch_route_with_waypoints(route_id):
    route = Route.objects.get(id=route_id)
    route_waypoints = RouteWaypoint.objects.filter(route=route)
    intermediates = []
    for route_waypoint in route_waypoints:
        intermediates.insert(
            route_waypoint.waypoint_position, 
            {"placeId": route_waypoint.waypoint.google_place_id}
        )

    url="https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline,routes.legs"
    }

    body = {
        "origin": {
            "placeId": route.origin.google_place_id
        },
        "destination": {
            "placeId": route.destination.google_place_id
        },
        "intermediates": intermediates,
        "travelMode": "DRIVE"
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()