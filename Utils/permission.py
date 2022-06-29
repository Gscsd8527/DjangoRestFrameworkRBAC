from rest_framework.permissions import BasePermission, SAFE_METHODS
import re
from django.conf import settings


class RBACPermission(BasePermission):
    """
    基于角色的认证系统的权限校验类
    """
    # message 默认是： 您没有执行该操作的权限。
    message = "没有访问该路径权限"  # 这里的message表示如果不通过权限的时候，错误提示信息

    def has_permission(self, request, view):
        permission_list = self._permission_list(request)
        print('用户： ', request.user.username)
        print('permission_list = ', permission_list)
        print('当前路径： ', request.path_info)
        # 判断这个路径是否是该用户能访问的
        cur_path = request.path_info

        # 白名单
        for reg in settings.PERMISSION_VALID_URL:
            if re.match(reg, cur_path):
                return None

        # 权限url列表
        for path in permission_list:
            if re.match(path, cur_path):
                return True
        return False

    @classmethod
    def _permission_list(self, request):
        """
        获取当前用户的权限url
        :param request:
        :return:
        """
        try:
            perms = request.user.roles.values(
                'permissions__url',
            ).distinct()
            return [p['permissions__url'] for p in perms]
        except AttributeError:
            return None


def permission_list(request):
    """
    获取权限列表: 组装权限列表，用于前端展示权限
    :return:
    """
    try:
        permission_list = request.user.roles.filter(permissions__id__isnull=False).values('permissions__id',
                                                                              'permissions__title',
                                                                              'permissions__url',
                                                                              'permissions__pid_id',
                                                                              'permissions__pid__url',
                                                                              'permissions__pid__title',
                                                                              'permissions__menu_id',
                                                                              'permissions__menu__name',
                                                                              'permissions__menu__icon',
                                                                              ).distinct()
        menu_dict = {}
        permission_dict = {}
        for item in permission_list:
            # 处理权限
            permission_dict[item['permissions__title']] = {
                'id': item['permissions__id'],
                'title': item['permissions__title'],
                'url': item['permissions__url'],
                'pid': item['permissions__pid_id'],
                'pid_url': item['permissions__pid__url'],
                'pid_name': item['permissions__pid__title'],
            }

            # 处理菜单
            menu_id = item['permissions__menu_id']
            if not menu_id:
                continue
            menu_node = {
                'id': item['permissions__id'],
                'title': item['permissions__title'],
                'url': item['permissions__url']
            }
            if menu_id in menu_dict:
                menu_dict[menu_id]['children'].append(menu_node)
            else:
                menu_dict[menu_id] = {
                    'title': item['permissions__menu__name'],
                    'icon': item['permissions__menu__icon'],
                    'children': [
                        menu_node
                    ]
                }

        return menu_dict, permission_dict
    except:
        return None


