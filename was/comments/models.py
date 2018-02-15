from django.db import models
from django.conf import settings
from django.utils import timezone

from customprofile.models import UserProfile
from stores.models import Notice


class NoticeComment(models.Model):
    text = models.TextField(blank=True)
    profile = models.ForeignKey(UserProfile, related_name='notice_comment_profile', on_delete=models.CASCADE)
    notice = models.ForeignKey('stores.Notice', related_name='notice_comment', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}::{} - {}".format(self.profile.user, self.notice.title,self.text)


class MenuComment(models.Model):
    text = models.TextField(blank=True)
    profile = models.ForeignKey(UserProfile, related_name='menu_comment_profile', on_delete=models.CASCADE)
    menu = models.ForeignKey('menus.Menu', related_name='menu_comment', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}::{}".format(self.profile.user, self.text)

    @property
    def owner(self):
        return self.profile.user


class ReviewComment(models.Model):
    text = models.TextField(blank=True)
    profile = models.ForeignKey(UserProfile, related_name='review_comment_profile', on_delete=models.CASCADE)
    review = models.ForeignKey('menus.Review', related_name='review_comment', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}::{}".format(self.profile.user, self.text)

    @property
    def owner(self):
        return self.profile.user