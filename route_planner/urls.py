from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.create_trip, name='create_trip'),
    path('<int:trip_id>/', views.get_trip, name='get_trip'),
    path('api/coordinates/', include('coordinates.urls')),
]