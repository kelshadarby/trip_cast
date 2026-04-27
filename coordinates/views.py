from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RestStop
from .serializers import CoordinateSetSerializer
from .services import get_place_coordinates

@api_view(['GET'])
def get_coordinate_set(request, rest_stop_id):
    try:
        rest_stop = RestStop.objects.get(id=rest_stop_id)
    except RestStop.DoesNotExist:
        return Response(
            {'error': 'Rest stop not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    google_place_id = request.query_params.get('place_id')

    if not google_place_id:
        return Response(
            {'error': 'place_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    coordinate_set_data = get_place_coordinates(google_place_id)

    if 'results' not in coordinate_set_data or not coordinate_set_data['results']:
        return Response(
            {'error': 'No coordinates found'},
            status=status.HTTP_404_NOT_FOUND
        )

    location = coordinate_set_data['results'][0]['geometry']['location']

    serializer = CoordinateSetSerializer(data={
        'rest_stop': rest_stop.id,
        'latitude': location['lat'],
        'longitude': location['lng']
    })

    if serializer.is_valid():
        serializer.save(rest_stop=rest_stop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
