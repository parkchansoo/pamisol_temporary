from django.conf.urls import url
from .views import LoginAPIView, RegistrationAPIView, LogoutAPIView

urlpatterns = [
    url(r'^signup/$', RegistrationAPIView.as_view()),
    url(r'^login/$', LoginAPIView.as_view()),
    url(r'^logout/$', LogoutAPIView.as_view()),
]