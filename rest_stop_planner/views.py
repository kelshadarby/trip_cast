import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Route
from .serializers import RestStopResultSerializer, RestStopSerializer
from route.serializers import RouteSerializer
from .services import get_rest_stop, get_place_coordinates, update_trip_with_intermediates

@api_view(['POST'])
def search_along_route(request, trip_id):
    text_query = request.data.get('textQuery')

    if not trip_id or not text_query:
        return Response(
            {'error': 'trip and textQuery are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    polyline = Route.objects.get(id=trip_id).polyline
    rest_stop_data = get_rest_stop(text_query, polyline)

    places = [
        {
            "google_place_id": rest_stop['id'],
            "name": rest_stop['displayName']['text'],
            "location_type": rest_stop['primaryTypeDisplayName'],
            "address": rest_stop['formattedAddress']
        }
        for rest_stop in rest_stop_data['places']
    ]

    serializer = RestStopResultSerializer(places, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_rest_stop(request, trip_id):
    try:
        trip = Route.objects.get(id=trip_id)
    except Route.DoesNotExist:
        return Response(
            {'error': 'Trip not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    coordinate_set_data = get_place_coordinates(request.data.get('google_place_id'))

    if 'results' not in coordinate_set_data or not coordinate_set_data['results']:
        return Response(
            {'error': 'No coordinates found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    coordinates = coordinate_set_data['results'][0]['geometry']['location']

    data = {
        "trip": trip.id,
        'google_place_id': request.data.get('google_place_id'),
        'name': request.data.get('name'),
        'location_type': request.data.get('location_type'),
        'address': request.data.get('address'),
        'latitude': coordinates['lat'],
        'longitude': coordinates['lng']
    }

    serializer = RestStopSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        updated_route = update_trip_with_intermediates(data['trip'], data['latitude'], data['longitude'])
        print("route update is hit")
        updated_route_serializer = RouteSerializer(data=updated_route)
        print("route update SERIALIZER is hit")
        if updated_route_serializer.is_valid():
            print("route update SERIALIZER is VALIDD")
            return Response(updated_route_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)