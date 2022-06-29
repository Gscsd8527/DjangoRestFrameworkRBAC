from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from apps.user.models import Permission
from Utils.permission import permission_list
from ..serializers.permission_serializer import PermissionSeralizer


class MenuTreeView(ListAPIView):
    """
    获取菜单结构
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSeralizer

    """
    重写list的方法，菜单的层级都在权限表中
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        try:
            menu_dict, permission_dict = permission_list(request)
            if menu_dict is None:
                results = {}
            else:
                results = menu_dict
        except:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

