from django.conf.urls import url
from rest_framework import views
from .views import  UserFeedsAPIView, StoreFeedsAPIView


urlpatterns = [
    url(r'^feeds/(?P<profile_pk>\d+)/user/$', UserFeedsAPIView.as_view(), name='feeds-user'),
    url(r'^feeds/(?P<profile_pk>\d+)/store/$', StoreFeedsAPIView.as_view(), name='feeds-store'),
]


# REGISTER_SUCCESS = 
# {
#     code: 1000
#     msg: "Register Success",
#     result: {
#         "eamil": "example@example.com",
#         "username": "example",
#         "is_shopkeeper": true
#     }
# }


# REGISTER_SUCCESS = 
# {
#     code: 1001,
#     msg: "Register Failure",
#     result: 
#     {
#         "result": false
#     }
# }

# LOGIN_SUCCESS = 
# {
#     code: 1010,
#     msg: "Login Success",
#     result: 
#     {
#         user: 
#         {
#             "user_id": "4",
#             "email": "kwon5604@naver.com",
#             "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
#         }
#     }
# }

# LOGIN_FAILURE =
# {
#     code: 1011,
#     msg: "Login Failure",
#     result:
#     {
#         "result": false
#     }
# }