from django.urls import path
from . import views

urlpatterns = [
    path('<int:rest_stop_id>/search/', views.get_coordinate_set, name='get_coordinate_set'),
]