from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import (
    UserProfileSerializer,
    DefaultUserProfileSerializer,
    StoreFollowingListSerializer,
    ReviewerFollowingListSerializer,
    UserFollowedListSerializer,
)
from .models import UserProfile
from rest_framework import permissions
from stores.permissions import IsOwnerOrReadOnly
from stores.models import Store
from basic_auth.models import User

from menus.serializers import MenuSerializer

from common import status_code
from search.models import SearchFilter

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserProfileRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'profile_pk'
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(UserProfileRudAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context
    
    def get_serializer(self,*args,**kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        status_code['PROFILE_DETAIL_SUCCESS']['data'] = serializer_class(*args, **kwargs).data
        return Response(status_code['PROFILE_DETAIL_SUCCESS'])

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset


class UserProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = DefaultUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(UserProfileListCreateAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args,**kwargs)
    
    def post(self, request, *args, **kwargs):
        request.POST['location_category']
        request.POST['food_category']
        request.FILES['image']
        print(request.FILES['image'])

        data = {}
        data['location_category'] = request.POST['location_category']
        data['food_category'] = request.POST['food_category']
        data['image'] = request.FILES['image']

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            print(serializer)
            obj = UserProfile.objects.get(user=self.request.user)

            name = 'userprofile'
            content_type = ContentType.objects.get(model=name)
            object_id = obj.pk
            SearchFilter.objects.create(content_type=content_type, object_id=object_id) 

            status_code['PROFILE_CREATE_SUCCESS']['data'] = serializer.data
            return Response(status_code['PROFILE_CREATE_SUCCESS'])
        else:
            return Response(status_code['PROFILE_CREATE_FAILURE'])


'''
chansoo edited this parts
those parts may need to fix permission_classes as auth_server does
'''
class FollowToggleAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, profile_pk, format=None):
        user_profile = UserProfile.objects.filter(pk=profile_pk)
        message = 'unfollowed'
        follow_status = UserProfile.objects.toggle_follow(request.user, user_profile)
        if follow_status:
            message = 'followed'
        status_code['FOLLOWING_TOGGLE_SUCCESS']['data'] = message
        return Response(status_code['FOLLOWING_TOGGLE_SUCCESS'])


class FollowingStoreListView(generics.ListAPIView):
    lookup_url_kwarg = 'profile_pk'
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StoreFollowingListSerializer

    def get_serializer(self,*args,**kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        status_code['FOLLOWING_STORE_LIST_CREATE_SUCCESS']['data'] = serializer_class(*args, **kwargs).data
        return Response(status_code['FOLLOWING_STORE_LIST_CREATE_SUCCESS'])

    def get_queryset(self):
        profile_pk = self.kwargs['profile_pk']
        obj_profile = UserProfile.objects.get(pk=profile_pk)
        return obj_profile.get_store_following()


class FollowingReviewerListView(generics.ListAPIView):
    lookup_url_kwarg = 'profile_pk'
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewerFollowingListSerializer
    # queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        status_code['FOLLOWING_REVIEWER_LIST_CREATE_SUCCESS']['data'] = serializer_class(*args, **kwargs).data
        return Response(status_code['FOLLOWING_REVIEWER_LIST_CREATE_SUCCESS'])

    def get_queryset(self):
        profile_pk = self.kwargs['profile_pk']
        obj_profile = UserProfile.objects.get(pk=profile_pk)
        return obj_profile.get_following()


class FollowedUserListView(generics.ListAPIView):
    lookup_url_kwarg = 'profile_pk'
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserFollowedListSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        status_code['FOLLOWED_USER_LIST_CREATE_SUCCESS']['data'] = serializer_class(*args, **kwargs).data
        return Response(status_code['FOLLOWED_USER_LIST_CREATE_SUCCESS'])

    def get_queryset(self):
        profile_pk = self.kwargs['profile_pk']
        obj_profile = UserProfile.objects.get(pk=profile_pk)
        return obj_profile.get_followed_user()



class KeepMenuListView(generics.ListAPIView):
    lookup_url_kwarg = 'profile_pk'
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuSerializer

    def get_queryset(self, *args, **kwargs):
        profile_pk = self.kwargs['profile_pk']
        my_profile = UserProfile.objects.get(pk=profile_pk)
        print('KeepMenuListView Stage 1: check my_profile: ')
        print(my_profile)
        qs_menu = my_profile.get_keep_menu()
        print('KeepMenuListView Stage 2: check qs_menu: ')
        print(qs_menu)
        return qs_menu