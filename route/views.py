from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RouteSerializer, RouteWaypointSerializer
from .services import fetch_route
from .models import Route, Waypoint, RouteWaypoint


def try_get_route(route_id):
    try:
        return Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({'error': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)


def try_get_waypoint(waypoint_id):
        try:
            return Waypoint.objects.get(id=waypoint_id)
        except Waypoint.DoesNotExist:
            return Response({'error': 'waypoint not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_route(request):
    origin_id = request.data.get('origin_waypoint_id', '')
    destination_id = request.data.get('destination_waypoint_id', '')
    try:
        origin = Waypoint.objects.get(id=origin_id)
        destination = Waypoint.objects.get(id=destination_id)
    except Waypoint.DoesNotExist:
        return Response({'error': 'Waypoint not found'}, status=status.HTTP_404_NOT_FOUND)

    route_data = fetch_route(origin.google_place_id, destination.google_place_id)

    if 'routes' not in route_data or not route_data['routes']:
        return Response({'error': 'No route found'}, status=status.HTTP_404_NOT_FOUND)
    
    route = route_data['routes'][0]

    db_route, created = Route.objects.get_or_create(
        origin=origin,
        destination=destination,
        defaults={
            'polyline': route.get('polyline', {}).get('encodedPolyline', ''),
            'total_distance_meters': route.get('distanceMeters', ''),
            'total_duration_seconds': route.get('duration', '')
        }
    )

    serializer = RouteSerializer(db_route)
    status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(serializer.data, status=status_code)


@api_view(['GET'])
def get_route(request, route_id):
    route = try_get_route(route_id)
    serializer = RouteSerializer(route)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_route_endpoints(request, route_id):
    route = try_get_route(route_id)
    new_origin_id = request.data.get('origin_waypoint_id')
    new_destination_id = request.data.get('destination_waypoint_id')

    origin = try_get_waypoint(new_origin_id) if new_origin_id else route.origin
    destination = try_get_waypoint(new_origin_id) if new_destination_id else route.destination

    route_data = fetch_route(origin.google_place_id, destination.google_place_id)

    if 'routes' not in route_data or not route_data['routes']:
        return Response({'error': 'No route found'}, status=status.HTTP_404_NOT_FOUND)

    new_route = route_data['routes'][0]

    route.origin = origin
    route.destination = destination
    route.polyline = new_route.get('polyline', {}).get('encodedPolyline', '')
    route.total_distance_meters = new_route.get('distanceMeters', '')
    route.total_duration_seconds = new_route.get('duration', '')
    route.save()

    serializer = RouteSerializer(route)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['DELETE'])
def delete_route(request, route_id):
    route = try_get_route(route_id)
    route.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_route_waypoint(request, route_id):
    route = try_get_route(route_id)
    waypoint_to_add = try_get_waypoint(request.data.get('waypoint_id'))
    route_waypoints = RouteWaypoint.objects.filter(route=route)
    last_waypoint = route_waypoints.latest('waypoint_position')
    
    added_route_waypoint, created = RouteWaypoint.objects.get_or_create(
        route=route,
        waypoint=waypoint_to_add,
        waypoint_position=(last_waypoint.waypoint_position + 1 if route_waypoints else 0)
    )

    route_with_waypoint = try_get_route(route_id)
    updated_route_data = fetch_route_with_waypoints(route_with_waypoint.id)

    if 'routes' not in updated_route_data or not updated_route_data['routes']:
        return Response({'error': 'No route found'}, status=status.HTTP_404_NOT_FOUND)

    updated_route = updated_route_data['routes'][0]

    route.polyline = updated_route.get('polyline', {}).get('encodedPolyline', '')
    route.total_distance_meters = updated_route.get('distanceMeters', '')
    route.total_duration_seconds = updated_route.get('duration', '')
    route.update()

    serializer = RouteSerializer(route)
    return Response(serializer.data, status=status.HTTP_200_OK)    
    
    
@api_view(['PATCH'])
def update_route_waypoint_position(request, route_id):
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({'error': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

    if RouteWaypoint.objects.get(route=route.id).exists():
        RouteWaypoint.objects.filter(route=route).latest("waypoint_position")