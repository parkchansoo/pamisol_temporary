from django.conf.urls import url, include
from django.contrib import admin
from .views import save_token, verify_token, expire_token

urlpatterns = [
    url(r'^save/$', save_token, name='save_token'),
    url(r'^verification/$', verify_token, name='verify_token'),
    url(r'^expiration/$', expire_token, name='expire_token'),
]