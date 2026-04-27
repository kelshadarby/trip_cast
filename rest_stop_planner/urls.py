from django.urls import path
from . import views

urlpatterns = [
    path('<int:trip_id>/search/', views.search_along_route, name='search_along_route'),
    path('<int:trip_id>/add/', views.add_rest_stop, name='add_rest_stop'),
]