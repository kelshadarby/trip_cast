from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WaypointSerializer, WaypointResultSerializer
from .services import find_waypoints

@api_view(['POST'])
def get_waypoint_results(request):
    text_query = request.data.get('textQuery')

    if not text_query:
        return Response(
            {'error': 'text_query is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    waypoint_data = find_waypoints(text_query)

    if 'places' not in waypoint_data or not waypoint_data['places']:
        return Response(
            {'error': 'No places found'},
            status=status.HTTP_404_NOT_FOUND
        )

    places = [
        {
            "name": place.get('displayName', {}).get('text', ''),
            "address": place.get('formattedAddress', ''),
            "location_type": place.get('primaryTypeDisplayName', {}).get('text', ''),
            "google_place_id": place.get('id', ''),
            "latitude": place.get('location', {}).get('latitude', None),
            "longitude": place.get('location', {}).get('longitude', None)
        }
        for place in waypoint_data['places']
    ]
    serializer = WaypointResultSerializer(places, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_waypoint(request):
    data = {
        "name": request.data.get('name', ''),
        "address": request.data.get('address', ''),
        "location_type": request.data.get('location_type', ''),
        "google_place_id": request.data.get('google_place_id', ''),
        "latitude": request.data.get('latitude', None),
        "longitude": request.data.get('longitude', None)
    }

    serializer = WaypointSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)