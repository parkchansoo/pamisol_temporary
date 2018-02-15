from django.conf.urls import url
from rest_framework import views
from menus import views


urlpatterns = [
    url(r'^store/(?P<store_pk>\d+)/menu/$', views.MenuAPIView.as_view(), name='menu-list_create'),
    url(r'^store/(?P<store_pk>\d+)/menu/(?P<menu_pk>\d+)/$', views.MenuRudAPIView.as_view(), name='menu-rud'),

    url(r'^store/(?P<store_pk>\d+)/menu/(?P<menu_pk>\d+)/menu_comment/$', views.MenuCommentAPIView.as_view(), name='menu-comment-list-create'),
    url(r'^store/(?P<store_pk>\d+)/menu/(?P<menu_pk>\d+)/menu_comment/(?P<menu_comment_pk>\d+)/$', views.MenuCommentRudAPIView.as_view(), name='menu-comment-edit'),
    url(r'^store/(?P<store_pk>\d+)/menu/(?P<menu_pk>\d+)/review/$', views.ReviewAPIView.as_view(), name='review-list-create'),
    url(r'^store/(?P<store_pk>\d+)/menu/(?P<menu_pk>\d+)/review/(?P<review_pk>\d+)/$', views.ReviewRudAPIView.as_view(), name='review-edit'),
    url(r'^store/(?P<store_pk>\d+)/menu/(?P<menu_pk>\d+)/review/(?P<review_pk>\d+)/review_comment/$', views.ReviewCommentAPIView.as_view(), name='review-comment-list-create')

]