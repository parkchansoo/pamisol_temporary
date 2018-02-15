from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^local_auth/', include("basic_auth.urls", namespace='basic_auth')),
    url(r'^social_auth/', include('rest_framework_social_oauth2.urls')),
]
