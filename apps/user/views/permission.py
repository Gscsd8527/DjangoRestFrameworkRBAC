from rest_framework.viewsets import ModelViewSet
from ..serializers.permission_serializer import PermissionSeralizer
from apps.user.models import Permission
from rest_framework.filters import SearchFilter, OrderingFilter


class PermissionViewSet(ModelViewSet):
    perms_map = ({'*': 'admin'}, {'*': 'permission_all'}, {'get': 'permission_list'}, {'post': 'permission_create'},
                 {'put': 'permission_edit'}, {'delete': 'permission_delete'})
    queryset = Permission.objects.all()
    serializer_class = PermissionSeralizer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name','id')
    ordering_fields = ('id',)
