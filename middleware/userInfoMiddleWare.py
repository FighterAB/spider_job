import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        # 判断路由请求是否为登录与注册
        # 如果是
        if path == '/myApp/login/' or path == '/myApp/regist/' or re.search('^/admin.*', path):
            return None
        # 如果没有session记录
        else:
            if not request.session.get('username'):
                return redirect('login')
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        return None

    def prcess_response(self, request, response):
        return response
