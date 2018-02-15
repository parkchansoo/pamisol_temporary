from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse_lazy

from rest_framework.response import Response

from customprofile.models import UserProfile
from search.models import SearchFilter


class StoreManager(models.Manager):
    def toggle_follow(self, request_user, obj_store):
        if obj_store in request_user.profile.get_store_following():
            request_user.profile.store_following.remove(obj_store)
            return False
        else:
            request_user.profile.store_following.add(obj_store)
            return True


class Store(models.Model):
    shopkeeper = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)
    image = models.ImageField(default='media/default_image.png')
    name = models.CharField(max_length=100)
    locations = models.TextField()
    phone = models.IntegerField()
    description = models.TextField()

    searchfilter = GenericRelation(SearchFilter, related_query_name='searchstore')

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = StoreManager()

    def __str__(self):
        return "{} - {}".format(self.shopkeeper.username, self.name)

    def get_latest_notice(self):
        print(self.store_notice)

    @property
    def owner(self):
        return self.shopkeeper




class NoticeManeger(models.Manager):
    def toggle_like(self, toggle_user, notice):
        notice = Notice.objects.get(notice=notice)
        toggle_profile = toggle_user.profile
        if toggle_profile in notice.like_user:
            notice.like_user.remove(toggle_profile)
            like_status = False
        else:
            notice.like_user.add(toggle_profile)
            like_status = False
        return like_status


class Notice(models.Model):
    store = models.ForeignKey('Store', related_name='store_notice', on_delete=models.CASCADE, null=False)
    image = models.ImageField(default='media/default_image.png')
    title = models.CharField(max_length=100, default='notice')
    text = models.TextField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_notice', blank=True)
    hit = models.PositiveIntegerField()
    storefeed = GenericRelation(SearchFilter, related_query_name='feednotice')

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = NoticeManeger()

    @property
    def owner(self):
        return self.store.shopkeeper

    def get_notice(self):
        return self.store.store_notice.all()

    def __str__(self):
        return "{} - {}".format(self.store, self.title) 

    def get_like_user(self):
        return self.like_user.all()

    def get_absolute_url(self):
        obj_store = self.notice.store
        return reverse_lazy('api-menus:notice-create-list', kwargs={'store_pk': obj_store.pk})