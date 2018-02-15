from django.conf.urls import url
from rest_framework import views
from stores import views


urlpatterns = [
    url(r'^register/store/$', views.StoreAPIView.as_view(), name='store-register'),
    url(r'^register/store/(?P<store_pk>\d+)/$', views.StoreEditView.as_view(), name='store-edit'),
    url(r'^store/(?P<store_pk>\d+)/$', views.StoreDetailView.as_view(), name='store-detial'),
    url(r'^store/(?P<store_pk>\d+)/notice/$', views.NoticeAPIView.as_view(), name='notice-create-list'),
    url(r'^store/(?P<store_pk>\d+)/notice/(?P<notice_pk>\d+)/$', views.NoticeEditView.as_view(), name='notice-edit'),
    url(r'^store/(?P<store_pk>\d+)/notice/(?P<notice_pk>\d+)/comment/$', views.NoticeCommentAPIView.as_view(), name='noticecomment-list-create'),
    url(r'^notice/(?P<notice_pk>\d+)/like/$', views.ToggleLikeNoticeAPIView.as_view(), name='notice-like'),
    url(r'^store/(?P<store_pk>\d+)/follow/$', views.FollowStoreToggleAPIView.as_view(), name='store-follow'),

    # review thumbnail in store detail
    url(r'^store/(?P<store_pk>\d+)/notice_thumbnail/$', views.StoreReviewThumbnailAPIView.as_view(), name='thumbnail-notice'),
]