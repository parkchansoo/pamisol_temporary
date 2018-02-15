from django.shortcuts import render
from rest_framework import views, generics
from .serializers import MenuSerializer, ReviewSerializer
from .models import Menu, Review, Store
from rest_framework import permissions
from stores.permissions import IsOwnerOrReadOnly

from comments.serializers import MenuCommentSerializer, ReviewCommentSerializer
from comments.models import MenuComment, ReviewComment


class MenuAPIView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        store_pk = self.kwargs['store_pk']
        store_obj = Store.objects.get(pk=store_pk)
        serializer.save(store=store_obj)

    def get_queryset(self):
        store_pk = self.kwargs['store_pk']
        return Menu.objects.filter(store_id__exact=store_pk)


class MenuRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'menu_pk'
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class MenuCommentAPIView(generics.ListCreateAPIView):

    serializer_class = MenuCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        menu_pk = self.kwargs['menu_pk']
        return MenuComment.objects.filter(menu_id__exact=menu_pk)

    def perform_create(self, serializer):
        menu_pk = self.kwargs['menu_pk']
        menu_obj = Menu.objects.get(pk=menu_pk)
        serializer.save(user=self.request.user, menu=menu_obj)


class MenuCommentRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'menu_comment_pk'
    queryset = MenuComment.objects.all()
    serializer_class = MenuCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ReviewAPIView(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []

    def get_queryset(self):
        menu_pk = self.kwargs['menu_pk']
        return Review.objects.filter(menu_id__exact=menu_pk)

    def perform_create(self, serializer):
        menu_pk = self.kwargs['menu_pk']
        menu_obj = Menu.objects.get(pk=menu_pk)
        serializer.save(user=self.request.user, menu=menu_obj)


class ReviewRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'review_pk'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class ReviewCommentAPIView(generics.ListCreateAPIView):

    serializer_class = ReviewCommentSerializer
    permission_classes = []

    def get_queryset(self):
        review_pk = self.kwargs['review_pk']
        return ReviewComment.objects.filter(review_id__exact=review_pk)

    def perform_create(self, serializer):
        review_pk = self.kwargs['review_pk']
        review_obj = Review.objects.get(pk=review_pk)
        serializer.save(user = self.request.user, review = review_obj)
