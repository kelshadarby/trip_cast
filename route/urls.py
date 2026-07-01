from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_route, name='create_route'),
    path('<int:route_id>/', views.get_route, name='get_route'),
    path('delete/<int:route_id>/', views.delete_route, name='delete_route'),
    path('update/endpoints/<int:route_id>/', views.update_route_endpoints, name='update_route_endpoints'),
]