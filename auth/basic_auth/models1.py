# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BasicAuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=254)
    is_shopkeeper = models.IntegerField()
    is_active = models.IntegerField()
    is_staff = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    login_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'basic_auth_user'


class BasicAuthUserGroups(models.Model):
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'basic_auth_user_groups'
        unique_together = (('user', 'group'),)


class BasicAuthUserUserPermissions(models.Model):
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'basic_auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CommentsMenucomment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    menu = models.ForeignKey('MenusMenu', models.DO_NOTHING)
    profile = models.ForeignKey('CustomprofileUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_menucomment'


class CommentsMenucommentLikeUser(models.Model):
    menucomment = models.ForeignKey(CommentsMenucomment, models.DO_NOTHING)
    userprofile = models.ForeignKey('CustomprofileUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_menucomment_like_user'
        unique_together = (('menucomment', 'userprofile'),)


class CommentsNoticecomment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    notice = models.ForeignKey('StoresNotice', models.DO_NOTHING)
    profile = models.ForeignKey('CustomprofileUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_noticecomment'


class CommentsNoticecommentLikeUser(models.Model):
    noticecomment = models.ForeignKey(CommentsNoticecomment, models.DO_NOTHING)
    userprofile = models.ForeignKey('CustomprofileUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_noticecomment_like_user'
        unique_together = (('noticecomment', 'userprofile'),)


class CommentsReviewcomment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    profile = models.ForeignKey('CustomprofileUserprofile', models.DO_NOTHING)
    review = models.ForeignKey('MenusReview', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_reviewcomment'


class CommentsReviewcommentLikeUser(models.Model):
    reviewcomment = models.ForeignKey(CommentsReviewcomment, models.DO_NOTHING)
    userprofile = models.ForeignKey('CustomprofileUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_reviewcomment_like_user'
        unique_together = (('reviewcomment', 'userprofile'),)


class CustomprofileUserprofile(models.Model):
    image = models.CharField(max_length=100)
    location_category = models.CharField(max_length=200, blank=True, null=True)
    food_category = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, unique=True)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'customprofile_userprofile'


class CustomprofileUserprofileFollowing(models.Model):
    userprofile = models.ForeignKey(CustomprofileUserprofile, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customprofile_userprofile_following'
        unique_together = (('userprofile', 'user'),)


class CustomprofileUserprofileStoreFollowing(models.Model):
    userprofile = models.ForeignKey(CustomprofileUserprofile, models.DO_NOTHING)
    store = models.ForeignKey('StoresStore', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customprofile_userprofile_store_following'
        unique_together = (('userprofile', 'store'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FeedsStorefeed(models.Model):
    object_id = models.IntegerField()
    updated_at = models.DateTimeField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    store = models.ForeignKey('StoresStore', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'feeds_storefeed'


class MenusMenu(models.Model):
    image = models.CharField(max_length=100)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    store = models.ForeignKey('StoresStore', models.DO_NOTHING)
    grade = models.CharField(max_length=10)
    hit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menus_menu'


class MenusMenuLikeUser(models.Model):
    menu = models.ForeignKey(MenusMenu, models.DO_NOTHING)
    userprofile = models.ForeignKey(CustomprofileUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menus_menu_like_user'
        unique_together = (('menu', 'userprofile'),)


class MenusReview(models.Model):
    image = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    menu = models.ForeignKey(MenusMenu, models.DO_NOTHING)
    profile = models.ForeignKey(CustomprofileUserprofile, models.DO_NOTHING)
    grade = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menus_review'


class MenusReviewLikeUser(models.Model):
    review = models.ForeignKey(MenusReview, models.DO_NOTHING)
    userprofile = models.ForeignKey(CustomprofileUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menus_review_like_user'
        unique_together = (('review', 'userprofile'),)


class StoresNotice(models.Model):
    image = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    store = models.ForeignKey('StoresStore', models.DO_NOTHING)
    hit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stores_notice'


class StoresNoticeLikeUser(models.Model):
    notice = models.ForeignKey(StoresNotice, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stores_notice_like_user'
        unique_together = (('notice', 'user'),)


class StoresStore(models.Model):
    image = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    locations = models.TextField()
    phone = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    shopkeeper = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stores_store'
