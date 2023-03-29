from celery import shared_task
from django.core.paginator import Paginator
from bbb.models import Usuarios
from bbb.api.serializers import UsuariosSerializer

@shared_task
def list_id(user_ids, page_size):
    queryset = Usuarios.objects.filter(id__in=user_ids)

    # Implementa a paginação
    paginator = Paginator(queryset, page_size)
    page = paginator.page(1)
    results = UsuariosSerializer(page, many=True).data
    return results
