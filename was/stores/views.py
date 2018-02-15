from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.serializers import NoticeCommentSerializer
from comments.models import NoticeComment

from feeds.models import StoreFeed

from stores.models import Store, Notice
from stores.serializers import StoreSerializer, NoticeSerializer, NoticeThumbnailSerializer
from stores.permissions import IsOwnerOrReadOnly
from search.models import SearchFilter


class StoreAPIView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(shopkeeper=self.request.user)
        obj = Store.objects.get(phone=serializer['phone'].value)

        name = 'store'
        content_type = ContentType.objects.get(model=name)
        object_id = obj.pk
        SearchFilter.objects.create(content_type=content_type, object_id=object_id)

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(StoreAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context


class StoreEditView(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = 'store_pk'

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(StoreEditView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context


class FollowStoreToggleAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, store_pk, format=None):
        store = Store.objects.get(pk=store_pk)
        message = 'unfollowed'
        follow_status = Store.objects.toggle_follow(request.user, store)
        if follow_status:
            message = 'followed'
        return Response(message)


class StoreDetailView(generics.RetrieveAPIView):
    lookup_url_kwarg = 'store_pk'

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(StoreDetailView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context


class StoreReviewThumbnailAPIView(generics.ListAPIView):
    serializer_class = NoticeThumbnailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        store_pk = self.kwargs['store_pk']
        qs = Notice.objects.filter(store=store_pk).order_by('-updated_at')[:3]
        return qs


class NoticeAPIView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        store_pk = self.kwargs['store_pk']
        return Notice.objects.filter(store__exact=store_pk)

    def perform_create(self, serializer):
        store_pk = self.kwargs['store_pk']
        store_obj = Store.objects.get(pk = store_pk)
        serializer.save(store=store_obj)


class NoticeEditView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'notice_pk'

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,]


class NoticeCommentAPIView(generics.ListCreateAPIView):
    serializer_class = NoticeCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        notice_pk = self.kwargs['notice_pk']
        return NoticeComment.objects.filter(notice_id__exact=notice_pk)

    def perform_create(self, serializer):
        notice_pk = self.kwargs['notice_pk']
        notice_obj = Notice.objects.get(pk=notice_pk)
        serializer.save(profile = self.request.user.profile, notice = notice_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ToggleLikeNoticeAPIView(APIView):
    permission_classes =[permissions.AllowAny]

    def get(self, request, notice_pk, format=None):
        notice = Notice.objects.filter(pk=notice_pk)
        message = 'review_dislike'
        like_status = Notice.objects.toggle_like(request.user, notice)
        if like_status:
            message = 'review_like'
        return Response(message, status=200)