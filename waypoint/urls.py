from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_waypoint_results, name='get_waypoint_results'),
    path('create/', views.create_waypoint, name='create_waypoint'),
]