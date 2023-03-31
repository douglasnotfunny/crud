import logging
import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Q

from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from bbb.models import Usuarios
from bbb.tasks import create_async
from .serializers import UsuariosSerializer


date = datetime.datetime.now()
year = date.year
month = date.month
day = date.day

class UsuariosPagination(PageNumberPagination):
    page_size = 10

class UsuariosViewSet(viewsets.ModelViewSet):
    serializer_class = UsuariosSerializer
    pagination_class = UsuariosPagination

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        print('list()')
        self.queryset = Usuarios.objects.all()
        return super(UsuariosViewSet, self).list(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        print("create()")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        self.queryset = Usuarios.objects.filter(pk=pk)
        obj = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Usuarios.objects.get(pk=kwargs['pk'])
        except Usuarios.DoesNotExist:
            raise NotFound('Object not found')

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
