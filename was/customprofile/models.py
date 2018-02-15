from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy

from basic_auth.models import User
from search.models import SearchFilter



class UserProfileManager(models.Manager):

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    # user.profile.following -- users i follow
    # user.followed_by -- users that follow me -- reverse relationship

    def toggle_follow(self, user, to_toggle):
        print('toggle_follow : ' + str(type(user)) + str(user))
        my_profile = self.get(user=user.pk)

        print('toggle_follow console_checking-1:  ')
        obj_user = to_toggle.first().user
        if obj_user in my_profile.following.all():
            my_profile.following.remove(obj_user)
            follow_status = False
        else:
            my_profile.following.add(obj_user)
            follow_status = True
        return follow_status

    def toggle_keep(self, user, toggle_menu):
        my_profile = self.get(user=user.pk)
        print('toggle_follow console_checking-1:  ')
        if toggle_menu in my_profile.keep_menu.all():
            my_profile.keep_menu.remove(toggle_menu)
            keep_status = False
        else:
            my_profile.keep_menu.add(toggle_menu)
            keep_status = True
        return keep_status

    def is_following(self, obj_user, followed_by_user):
        obj_user_profile = self.get(user=obj_user)
        if followed_by_user in obj_user_profile.following.all():
            return True
        else:
            return False


class UserProfile(models.Model):
    user                = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile') # user.profile 
    image               = models.ImageField(default='media/default_image.png')
    description = models.TextField()
    location_category = models.CharField(max_length=200, blank=True, null=True)

    following           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followers')
    store_following     = models.ManyToManyField("stores.Store", blank=True, related_name='store_followers')
    keep_menu           = models.ManyToManyField("menus.Menu", blank=True, related_name='keep_profile')

    food_category       = models.CharField(max_length=200, blank=True, null=True)

    searchfilter = GenericRelation(SearchFilter, related_query_name='searchprofile')

    objects = UserProfileManager() # UserProfile.objects.all()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    def get_following(self):
        users  = self.following.all() # User.objects.all().exclude(username=self.user.username)
        return users.exclude(username=self.user.username)

    def get_store_following(self):
        stores = self.store_following.all()
        return stores

    def get_keep_menu(self):
        menu = self.keep_menu.all()
        return menu

    def get_followed_user(self):
        followed_users = self.user.followers
        return followed_users.exclude(user=self.user)

    @property
    def owner(self):
        return self.user


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)
        # celery + redis
        # deferred task

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)