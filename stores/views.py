from django.shortcuts import render

from django.shortcuts import get_object_or_404
from stores.models import Store, Notice
from stores.serializers import StoreSerializer, NoticeSerializer
from stores.permissions import IsOwnerOrReadOnly
from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status


class StoreAPIView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(shopkeeper=self.request.user)


class StoreEditView(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = 'store_pk'

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class StoreDetailView(generics.RetrieveAPIView):
    lookup_url_kwarg = 'store_pk'

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class NoticeAPIView(generics.ListCreateAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        ]

# class HitNoticeLike(generics.CreateAPIView):
#     lookup_url_kwarg = 'notice_pk'
#


@api_view(['GET', 'POST'])
def hit_notice_like(request, foramt=None):
     serializer = NoticeSerializer(data=request.data)
     if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)