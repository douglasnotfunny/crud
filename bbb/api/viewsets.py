from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


from rest_framework.renderers import JSONRenderer
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from bbb.models import Usuarios
from bbb.tasks import list_id
from .serializers import UsuariosSerializer


class UsuariosPagination(PageNumberPagination):
    page_size = 2

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    pagination_class = UsuariosPagination
    renderer_classes = [JSONRenderer]

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*2))
    def dispatch(self, *args, **kwargs):
        user_ids = self.queryset.values_list('id', flat=True)
        result = list_id.delay(list(user_ids), 2)
        print("Task id in Celery", result)
        return super(UsuariosViewSet, self).dispatch(*args, **kwargs)
