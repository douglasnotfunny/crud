from celery import shared_task
from rest_framework.response import Response
from rest_framework import status
from .api.serializers import UsuariosSerializer

@shared_task
def create_async(data):
    serializer = UsuariosSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
