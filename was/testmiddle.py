from django.conf import settings
from django.db import connection
from django.template import Template, Context
import requests
from django.http import HttpResponse
import json
from ipware.ip import get_ip
from django.http import JsonResponse
from common import status_code

class SimpleMiddleware(object):
    def __init__(self):
        pass
        # One-time configuration and initialization.

    def process_request(self, request):
        if request.META.get("HTTP_AUTHORIZATION",None) != None:
            token = request.META['HTTP_AUTHORIZATION']
            if token.split(" ")[0] == 'Token':
                token = token.split(" ")[1]

                ip = get_ip(request)
                payload = {'token':token,'ip':ip}
                response = requests.post("http://192.168.0.10:8002/token/verification/", data=payload)

                msg = json.loads(response.text)

                if response.status_code == 200 and msg['code'] == 1040:
                    return None
                else:
                    return JsonResponse(status_code['AUTH_FAILURE'])
            elif token.split(" ")[0] == 'Bearer':
                return None
        else:
            return HttpResponse("<h1>No Token!</h1>",status=401)


    def process_view(self, request, view_func, view_args, view_kwargs):

        respose = None
        return respose

    def process_template_response(self, request, response):

        return response

    def process_response(self,request, response):

        return response