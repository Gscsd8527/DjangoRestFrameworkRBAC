from django.conf.urls import url
from .views.user import UserRegisterView, UserAuthView, UserInfoView, UserListView
from .views.menu import MenuTreeView
from .views.role import RoleViewSet
from rest_framework import routers
from .views import permission
from django.urls import include
app_name = 'user'

router = routers.SimpleRouter()
router.register(r'permissions', permission.PermissionViewSet, basename="permissions")
router.register(r'roles', RoleViewSet, basename="roles")


urlpatterns = [
    url(r'auth/register/', UserRegisterView.as_view(), name='register'),
    url(r'auth/login/', UserAuthView.as_view(), name='login'),
    url(r'auth/info/', UserInfoView.as_view(), name='info'),

    # 用户管理
    url(r'api/user/list/', UserListView.as_view(), name='user_list'),

    # 菜单
    url(r'api/menu/tree/', MenuTreeView.as_view(), name='menus_tree'),

    url(r'api/', include(router.urls)),
]