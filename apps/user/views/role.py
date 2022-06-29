from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from apps.user.models import Role
from ..serializers.role_serializer import RoleSerializer
from Utils.pagination import CustomPageNumberPagination


class RoleViewSet(ModelViewSet):
    """
    角色管理：增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'role_all'}, {'get': 'role_list'}, {'post': 'role_create'}, {'put': 'role_edit'},
                 {'delete': 'role_delete'})
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title',)
    ordering_fields = ('id',)