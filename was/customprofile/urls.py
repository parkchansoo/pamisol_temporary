from django.conf.urls import url, include

from django.views.generic.base import RedirectView

from .views import (
    UserProfileRudAPIView,
    UserProfileListCreateAPIView,
    FollowToggleAPIView,
    FollowingStoreListView,
    FollowingReviewerListView,
    FollowedUserListView,
    KeepMenuListView,
    )

urlpatterns = [

    url(r'^(?P<profile_pk>\d+)/$', UserProfileRudAPIView.as_view(), name='profile-detail'),
    url(r'^$', UserProfileListCreateAPIView.as_view(), name='profile-list-create'),

    url(r'^(?P<profile_pk>\d+)/follow/$', FollowToggleAPIView.as_view(), name='toggle-follow'),
    url(r'^(?P<profile_pk>\d+)/follow_store_list/$', FollowingStoreListView.as_view(), name='follow-store-list'),
    url(r'^(?P<profile_pk>\d+)/follow_reviewer_list/$', FollowingReviewerListView.as_view(), name='follow-reviewer-list'),
    url(r'^(?P<profile_pk>\d+)/followed_user_list/$', FollowedUserListView.as_view(), name='followed-user-list'),
    url(r'^(?P<profile_pk>\d+)/keep/$', KeepMenuListView.as_view(), name='keep-menu'),
]