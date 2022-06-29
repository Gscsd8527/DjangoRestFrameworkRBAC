from django.utils.deprecation import MiddlewareMixin
from Utils.permission import permission_list
import re
from django.shortcuts import HttpResponse
"""
中间件用在restframework中并且还有jwt认证模式，又使用认证系统和权限，两个功能有冲突，
"""

FILTER_PATH = [
    "/info",
    "/api",
    "/auth",
]

"""
测试JWT和中间件配合使用
"""
class RBACMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        request_ip = request.META['REMOTE_ADDR']  # 获取请求IP
        request_url = request.path_info  # 获取请求URL

        # 拦截指定路径
        for filter_path in FILTER_PATH:
            if re.match(filter_path, request_url):
                return None
        else:
            return HttpResponse("路径不是允许放行的路径")

