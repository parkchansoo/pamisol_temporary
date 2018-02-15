# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


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
    is_active = models.IntegerField()
    is_staff = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

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
    menu = models.ForeignKey('MenusMenu', models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_menucomment'


class CommentsMenucommentLike(models.Model):
    menucomment = models.ForeignKey(CommentsMenucomment, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_menucomment_like'
        unique_together = (('menucomment', 'user'),)


class CommentsNoticecomment(models.Model):
    text = models.TextField()
    notice = models.ForeignKey('StoresNotice', models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_noticecomment'


class CommentsNoticecommentLike(models.Model):
    noticecomment = models.ForeignKey(CommentsNoticecomment, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_noticecomment_like'
        unique_together = (('noticecomment', 'user'),)


class CommentsReviewcomment(models.Model):
    text = models.TextField()
    review = models.ForeignKey('MenusReview', models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_reviewcomment'


class CommentsReviewcommentLike(models.Model):
    reviewcomment = models.ForeignKey(CommentsReviewcomment, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_reviewcomment_like'
        unique_together = (('reviewcomment', 'user'),)


class CustomprofileUserprofile(models.Model):
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING, unique=True)
    image = models.CharField(max_length=100)

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


class MenusMenu(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    image = models.CharField(max_length=100)
    price = models.IntegerField()
    store = models.ForeignKey('StoresStore', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menus_menu'


class MenusReview(models.Model):
    text = models.TextField()
    image = models.CharField(max_length=100)
    menu = models.ForeignKey(MenusMenu, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menus_review'


class Oauth2ProviderAccesstoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.ForeignKey('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=255)
    scope = models.TextField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderRefreshtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    access_token = models.ForeignKey(Oauth2ProviderAccesstoken, models.DO_NOTHING, unique=True)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.SmallIntegerField()
    backend = models.CharField(max_length=32)
    data = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


class StoresNotice(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.CharField(max_length=100)
    store = models.ForeignKey('StoresStore', models.DO_NOTHING)

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
    name = models.CharField(max_length=100)
    locations = models.TextField()
    phone = models.IntegerField()
    description = models.TextField()
    image = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    shopkeeper = models.ForeignKey(BasicAuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stores_store'
