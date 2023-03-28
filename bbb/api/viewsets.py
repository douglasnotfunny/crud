from rest_framework import viewsets, mixins
from .serializers import UsuariosSerializer
from bbb.models import Usuarios

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
