import logging
import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Q

from rest_framework.renderers import JSONRenderer
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from bbb.models import Usuarios
from bbb.tasks import list_id
from .serializers import UsuariosSerializer


date = datetime.datetime.now()
year = date.year
month = date.month
day = date.day

class UsuariosPagination(PageNumberPagination):
    page_size = 2

class UsuariosViewSet(viewsets.ModelViewSet):
    serializer_class = UsuariosSerializer
    pagination_class = UsuariosPagination

    def get_queryset(self):
        print('get_queryset()')
        queryset = None

        if self.request.method == 'GET':
            cpf = self.request.GET.get('cpf', '')
            full_name = self.request.GET.get('full_name', '')
            state = self.request.GET.get('state', '')
            city = self.request.GET.get('city', '')
            start_date = self.request.GET.get('start_date', datetime.date(year-18, month, day))
            end_date = self.request.GET.get('end_date', datetime.date(year-70, month, day))

            if cpf or full_name or state or city:
                print('get_queryset().FILTER')
                queryset = Usuarios.objects.filter(Q(cpf=cpf)|
                                                   Q(full_name=full_name)|
                                                   Q(state=state)|
                                                   Q(born_date__gt=start_date)|
                                                   Q(born_date__lt=end_date))
            else:
                print('get_queryset().ALL')
                queryset = Usuarios.objects.all()

        return queryset

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        print('list()')
        user_ids = self.get_queryset().values_list('id', flat=True)
        result = list_id.delay(list(user_ids), 2)
        print("Task id in Celery", result)
        return super(UsuariosViewSet, self).list(*args, **kwargs)
