from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Route
from .serializers import RouteSerializer
from .services import get_route

@api_view(['POST'])
def create_trip(request, save=False):
    origin = request.data.get('origin').get('address')
    destination = request.data.get('destination').get('address')

    if not origin or not destination:
        return Response(
            {'error': 'origin and destination are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    route_data = get_route(origin, destination)

    if 'routes' not in route_data or not route_data['routes']:
        return Response(
            {'error': 'No route found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # route = route_data['routes'][0]

    route = Route.objects.create(
        origin=origin,
        destination=destination,
        polyline=route['polyline']['encodedPolyline'],
        total_distance_meters=route['distanceMeters'],
        total_duration_seconds=int(route['duration'].replace('s', '')),
    )

    serializer = RouteSerializer(route)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
