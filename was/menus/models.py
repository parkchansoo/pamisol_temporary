from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse, reverse_lazy

from stores.models import Store
from customprofile.models import UserProfile
from feeds.models import StoreFeed
from search.models import SearchFilter


class MenuManager(models.Manager):
    def toggle_like(self, toggle_user, menu):
        menu = menu.first()
        toggle_profile = toggle_user.profile

        if toggle_profile in menu.like_user.all():
            menu.like_user.remove(toggle_profile)
            like_status = False
        else:
            menu.like_user.add(toggle_profile)
            like_status = True
        return like_status


class Menu(models.Model):
    store = models.ForeignKey('stores.Store', related_name='menu', on_delete=models.CASCADE)
    image = models.ImageField(default='media/default_image.png')
    name = models.CharField(max_length=40, default='default menu')
    description = models.TextField()
    price = models.IntegerField()
    like_user = models.ManyToManyField(UserProfile, related_name='menu_like')
    grade = models.CharField(max_length=10)
    hit = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=200, default='None')

    searchfilter = GenericRelation(SearchFilter, related_query_name='searchmenu')
    storefeed = GenericRelation(SearchFilter, related_query_name='feedstore')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MenuManager()


    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.store.shopkeeper

    def get_like_user(self):
        return self.like_user.all()

    def get_hit(self):
        print('get_hit: ' + str(self.hit) + ', type is ' + str(type(self.hit)))
        self.hit = self.hit + 1
        print('get_hit: ' + str(self.hit) + ', type is ' + str(type(self.hit)))


class ReviewManager(MenuManager):
    def toggle_like(self, toggle_user, review):
        review = review.first()
        toggle_profile = toggle_user.profile
        if toggle_profile in review.like_user.all():
            review.like_user.remove(toggle_profile)
            like_status = False
        else:
            review.like_user.add(toggle_profile)
            like_status = True
        return like_status


class Review(models.Model):
    menu = models.ForeignKey('Menu', related_name='menu_review', on_delete=models.CASCADE)
    image = models.ImageField(default='media/default_image.png')
    text = models.TextField()
    profile = models.ForeignKey(UserProfile, related_name='reviews', on_delete=models.CASCADE)
    like_user = models.ManyToManyField(UserProfile, related_name='review_like')
    grade = models.PositiveIntegerField(validators=[MaxValueValidator(5)], default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "{} - {} - {}".format(self.menu ,self.profile.user, self.text)

    @property
    def owner(self):
        return self.profile.user

    def get_reviews(self):
        return self.profile.profile_review.all()

    def get_like_user(self):
        return self.like_user.all()

    def get_closest_like(self, request_user):
        # close_likes = self.like_user.all()
        # for like_profile in close_likes:
        #     if like_profile in request_user.following:
        #         close_likes = [like_profile]
        return self.like_user.first()

    def get_absolute_url(self):
        menu = self.menu
        return reverse_lazy('api-menus:review-edit', kwargs={'review_pk': self.pk, 'menu_pk': menu.pk, 'store_pk': menu.store.pk})

    def get_absolute_menu_url(self):
        menu = self.menu
        return reverse_lazy('api-menus:menu-rud', kwargs={'menu_pk': menu.pk, 'store_pk': menu.store.pk})