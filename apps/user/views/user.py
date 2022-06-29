from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from Utils.response import resp_error_status, resp_success_status
from Utils.permission import permission_list
from apps.user.models import User
from apps.user.serializers.user_serializer import UserInfoListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegisterView(APIView):
    """
    用户注册视图
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if all([username, password]):
            # 使用  create_user 会自动把密码加密，这样我们再效验的时候可以用 authenticate 来校验是否登录
            user = User.objects.create_user(username=username, password=password)
            user.is_active = True  # 激活
            user.save()

            # 签发token
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            resp = resp_success_status(msg="注册", token=token)
            return Response(resp)
        else:
            resp = resp_error_status(msg="用户名密码漏填")
            return Response(resp, status=403)


class UserAuthView(APIView):
    """
    用户认证
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # 签发token
            payload = jwt_payload_handler(user)  # 这个 payload 返回的值就是 我们在 setting 中 配置的 JWT_RESPONSE_PAYLOAD_HANDLER
            token = jwt_encode_handler(payload)
            resp = resp_success_status(msg="登录", token=token)
        else:
            resp = resp_error_status(msg="登录失败")
        return Response(resp)


class UserInfoView(APIView):
    """
    获取当前用户的菜单和权限
    """
    permission_classes = ()

    def get(self, request):
        if request.user.id is not None:
            menu_dict, permission_dict = permission_list(request)
            if menu_dict is None:
                return Response(resp_success_status('获取权限'))
            data_json = {
                'menu': menu_dict,
                'permission': permission_dict,
            }
            return Response(resp_success_status('获取权限', **data_json))
        else:
            return Response(resp_error_status(msg='用户名或密码错误!'))


class UserListView(ListAPIView):
    """
    获取该用户管辖的所有用户
    """
    queryset = User.objects.filter(is_delete=False, is_superuser=False) # 过滤掉无效用户和超级用户
    serializer_class = UserInfoListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name', 'id')  # 可以通过name 或 id 检索
    ordering_fields = ('id',)

    """
    重写list方法
    """
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def _filter_queryset(self, request):
        """
        过滤queryset
        如果：
            用户为：超级用户： 就返回所有用户
            用户为：管理层，那么就返回该管理层其它角色下对应的所有用户， 比如：张三角色为管理层和技术部门，那么就返回技术部所有用户
           普通用户： 返回自己下级（usermodel中有一个字段为上级主管）
        """
        if request.user.is_superuser:
            return User.objects.filter(is_delete=False, is_superuser=False)
        # else:
        #     user_id = User.objects.get(pk=request.user.id)
        #     roles_titles = User.objects.get(pk=request.user.id).roles.values_list("title")
