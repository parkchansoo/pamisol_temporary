from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token/', include('redis_session.urls', namespace='redis_session')),
]
