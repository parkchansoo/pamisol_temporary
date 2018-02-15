from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MenuSerializer, ReviewSerializer
from .models import Menu, Review

from storetry.paginations import ReviewOnMenuPagination, CommentPagination
from customprofile.models import UserProfile
from comments.serializers import MenuCommentSerializer, ReviewCommentSerializer
from comments.models import MenuComment, ReviewComment
from stores.permissions import IsOwnerOrReadOnly
from stores.models import Store
from search.models import SearchFilter


'''
menu related api views
'''
class MenuAPIView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = ReviewOnMenuPagination

    def perform_create(self, serializer):
        store_pk = self.kwargs['store_pk']
        store_obj = Store.objects.get(pk=store_pk)
        serializer.save(store=store_obj)
        
        obj = Menu.objects.last()
        name = 'menu'
        content_type = ContentType.objects.get(model=name)
        object_id = obj.pk
        SearchFilter.objects.create(content_type=content_type, object_id=object_id)

    def get_queryset(self):
        store_pk = self.kwargs['store_pk']
        return Menu.objects.filter(store_id__exact=store_pk)

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(MenuAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context


class LikeToggleMenuAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, menu_pk, format=None):
        menu = Menu.objects.filter(pk=menu_pk)
        message = 'dislike'
        like_status = Menu.objects.toggle_like(request.user, menu)
        if like_status:
            message = 'like'
        return Response(message, status=200)


class MenuRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'menu_pk'
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        menu_pk = self.kwargs['menu_pk']
        print('MenuRudAPIView-get_queryset: ')
        qs = Menu.objects.filter(id=menu_pk)
        obj_menu = qs.first()
        obj_menu.hit += 1
        obj_menu.save()
        return qs

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(MenuRudAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context



class ToggleKeepMenuAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, menu_pk, format=None):
        toggle_menu = Menu.objects.get(pk=menu_pk)
        message = 'out keep list'
        keep_status = UserProfile.objects.toggle_keep(request.user, toggle_menu)
        if keep_status:
            message = 'in keep list'
        return Response(message)
        # status_code['FOLLOWING_TOGGLE_SUCCESS']['data'] = message
        # return Response(status_code['FOLLOWING_TOGGLE_SUCCESS'])


class MenuCommentAPIView(generics.ListCreateAPIView):
    serializer_class = MenuCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination

    def get_queryset(self):
        menu_pk = self.kwargs['menu_pk']
        return MenuComment.objects.filter(menu_id__exact=menu_pk)

    def perform_create(self, serializer):
        menu_pk = self.kwargs['menu_pk']
        menu_obj = Menu.objects.get(pk=menu_pk)
        serializer.save(profile=self.request.user.profile, menu=menu_obj)


class MenuCommentRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'menu_comment_pk'
    queryset = MenuComment.objects.all()
    serializer_class = MenuCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ReviewAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewOnMenuPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_queryset(self):
        menu_pk = self.kwargs['menu_pk']
        return Review.objects.filter(menu_id__exact=menu_pk)

    def perform_create(self, serializer):
        menu_pk = self.kwargs['menu_pk']
        menu_obj = Menu.objects.get(pk=menu_pk)
        print(serializer)
        print(menu_obj)
        serializer.save(profile=self.request.user.profile, menu=menu_obj)

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(ReviewAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context


class LikeToggleReviewAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, review_pk, format=None):
        rewview = Review.objects.filter(pk=review_pk)
        message = 'review_dislike'
        like_status = Menu.objects.toggle_like(request.user, rewview)
        if like_status:
            message = 'review_ike'
        return Response(message, status=200)


class ReviewRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'review_pk'
    queryset = Review.objects.all()

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = CommentPagination

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(ReviewRudAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context


class ReviewCommentAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        review_pk = self.kwargs['review_pk']
        return ReviewComment.objects.filter(review_id__exact=review_pk)

    def perform_create(self, serializer):
        review_pk = self.kwargs['review_pk']
        review_obj = Review.objects.get(pk=review_pk)
        serializer.save(profile = self.request.user.profile, review = review_obj)


'''
    class StandardResultsSetPagination(PageNumberPagination):
        page_size = 2
        page_size_query_param = 'page_size'
        max_page_size = 1000
'''