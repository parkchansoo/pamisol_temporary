from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

import jwt
from datetime import datetime
from ipware.ip import get_ip

from common import status_code


@csrf_exempt
def save_token(request):
    
    header_token = request.META['HTTP_AUTHORIZATION']
    token = header_token.split(" ")[1]
    decode_token = jwt.decode(token,settings.AUTH_SECRET_KEY,algorithms=['HS256'])    

    ip = get_ip(request)
    timeout = decode_token['exp'] - int(datetime.now().strftime('%s'))

    info = (token,ip)
    cache.set(decode_token['id'],info,timeout=timeout)

    return JsonResponse(status_code['SAVE_TOKEN_SUCCESS'])


@csrf_exempt
def verify_token(request):

    token = request.POST.get('token')
    ip = request.POST.get('ip')
    print(token)
    
    try:
        decode_token = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=['HS256'])
        
    except:
        return JsonResponse(status_code['VERIFY_TOKEN_FAILURE'])

    #timeout = decode_token['exp'] - int(datetime.now().strftime('%s'))
    info = (token,ip)

    if cache.get(decode_token['id'])[0] == token:
        timeout = decode_token['exp'] - int(datetime.now().strftime('%s'))
        cache.set(decode_token['id'],info,timeout=timeout)

        return JsonResponse(status_code['VERIFY_TOKEN_SUCCESS'])

    else:
        return JsonResponse(status_code['VERIFY_TOKEN_FAILURE'])


@csrf_exempt
def expire_token(request):

    token = request.POST.get('token')
    
    try:
        decode_token = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=['HS256'])
    except:
        return JsonResponse(status_code['EXPIRE_TOKEN_FAILURE'])
    
    if cache.get(decode_token['id'])[0] == token:
        timeout = decode_token['exp'] - int(datetime.now().strftime('%s'))
        cache.expire(decode_token['id'], 0)
        return JsonResponse(status_code['EXPIRE_TOKEN_SUCCESS'])

    else:
        return JsonResponse(status_code['EXPIRE_TOKEN_FAILURE'])