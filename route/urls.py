from django.urls import path, include
from . import views

urlpatterns = [
    path('create_trip/', views.create_trip, name='create_trip'),
]