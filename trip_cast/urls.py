from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/routes/', include('route_planner.urls')),
    path('api/rest_stops/', include('rest_stop_planner.urls')),
]
