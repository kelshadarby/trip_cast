from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trip, Waypoint
from .serializers import TripSerializer
from .services import get_route

@api_view(['POST'])
def create_trip(request):
    origin = request.data.get('origin')
    destination = request.data.get('destination')
    departure_date = request.data.get('departure_date')

    if not origin or not destination or not departure_date:
        return Response(
            {'error': 'origin, destination and departure_date are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # call google routes api
    route_data = get_route(origin, destination)

    if 'routes' not in route_data or not route_data['routes']:
        return Response(
            {'error': 'No route found'},
            status=status.HTTP_404_NOT_FOUND
        )

    route = route_data['routes'][0]

    # save trip to database
    trip = Trip.objects.create(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        polyline=route['polyline']['encodedPolyline'],
        total_distance_meters=route['distanceMeters'],
        total_duration_seconds=int(route['duration'].replace('s', ''))
    )

    serializer = TripSerializer(trip)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_trip(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return Response(
            {'error': 'Trip not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TripSerializer(trip)
    return Response(serializer.data, status=status.HTTP_200_OK)