from django.conf.urls import url, include


from .views import SearchFilterAPIView, RecommendAPIView

urlpatterns = [

    url(r'^$',SearchFilterAPIView.as_view(), name='search-filter'),
    url(r'^recommend_list/$',RecommendAPIView.as_view(), name='search-recommend-list'),
]