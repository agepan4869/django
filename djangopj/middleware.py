# middleware.py

import logging
from django.http import HttpResponseForbidden
from .allow_IPs import *

logger = logging.getLogger(__name__)



class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        logger.info(f'Request from IP: {ip}')  # ここでIPアドレスをログに出力
        if not any(self.ip_in_range(ip, allowed_ip) for allowed_ip in ALLOWED_IPS):
            logger.warning(f'IP {ip} is not allowed')  # 許可されていない場合の警告ログ
            return HttpResponseForbidden("You are not allowed to access this site.")
        return self.get_response(request)

    def ip_in_range(self, ip, allowed_ip):
        if '/' in allowed_ip:
            from ipaddress import ip_network, ip_address
            return ip_address(ip) in ip_network(allowed_ip)
        return ip == allowed_ip
