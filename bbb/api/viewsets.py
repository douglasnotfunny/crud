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
    serializer_class = UsuariosSerializer
    pagination_class = UsuariosPagination
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        queryset = Usuarios.objects.all()
        if self.request.method == 'GET':
            # faça a filtragem necessária apenas no caso de GET
            cpf = self.request.GET.get('cpf', None)
            if cpf:
                queryset = queryset.filter(cpf=cpf)
        return queryset

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        user_ids = self.get_queryset().values_list('id', flat=True)
        result = list_id.delay(list(user_ids), 2)
        print("Task id in Celery", result)
        return super(UsuariosViewSet, self).list(*args, **kwargs)
