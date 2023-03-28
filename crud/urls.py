from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from bbb.api import viewsets as bbb_viewsets

route = routers.DefaultRouter()
route.register(r'usuarios', bbb_viewsets.UsuariosViewSet, basename="Usuario")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls)),
    path('api/', include(route.urls))
]
