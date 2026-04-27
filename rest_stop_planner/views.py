from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trip
from .serializers import RestStopResultSerializer, RestStopSerializer
from .services import get_rest_stop

@api_view(['POST'])
def search_along_route(request, trip_id):
    text_query = request.data.get('textQuery')

    if not trip_id or not text_query:
        return Response(
            {'error': 'trip and textQuery are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    polyline = Trip.objects.get(id=trip_id).polyline
    rest_stop_data = get_rest_stop(text_query, polyline)

    places = [
        {
            "google_place_id": rest_stop['id'],
            "name": rest_stop['displayName']['text'],
            "location_type": rest_stop['primaryType'],
            "address": rest_stop['formattedAddress']
        }
        for rest_stop in rest_stop_data['places']
    ]

    serializer = RestStopResultSerializer(places, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_rest_stop(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return Response(
            {'error': 'Trip not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    data = {
        "trip": trip.id,
        'google_place_id': request.data.get('google_place_id'),
        'name': request.data.get('name'),
        'location_type': request.data.get('location_type'),
        'address': request.data.get('address'),
    }

    serializer = RestStopSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)