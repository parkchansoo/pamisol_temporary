from django.urls import reverse_lazy

from rest_framework import serializers
from rest_framework.serializers import(
    SerializerMethodField
)

from .models import Menu, Review


class MenuSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    like_btn = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    like_user = serializers.StringRelatedField(many=True, source='get_like_user', read_only=True)
    like_user_count = SerializerMethodField()

    keep_btn = serializers.SerializerMethodField()
    keep_status = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'pk',
            'image',
            'name',
            'description',
            'price',
            'hit',
            'updated_at',

            'like_btn',
            'like_user',
            'like_status',
            'like_user_count',

            'keep_btn',
            'keep_status',
        ]

        read_only_fields = [
            'created_at',
            'updated_at'
        ]

    def get_like_btn(self, obj):
        return reverse_lazy('api-menus:like-menu', kwargs={'menu_pk': obj.pk})

    def get_like_user_count(self, obj):
        return obj.like_user.count()

    def get_keep_btn(self, obj):
        return reverse_lazy('api-menus:keep-menu', kwargs={'menu_pk': obj.pk})

    def get_like_status(self, obj):
        request = self.context.get('__request')
        print('get_like_status Stage 1: ')
        print(request)
        obj_profile = request.user.profile
        if obj_profile in obj.like_user.all():
            return True
        return False

    def get_keep_status(self, obj):
        request = self.context.get('__request')
        obj_profile = request.user.profile
        if obj_profile in obj.keep_profile.all():
            return True
        return False


class ReviewSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    menu_url = serializers.SerializerMethodField()
    image = serializers.ImageField()
    menu = SerializerMethodField()
    profile = SerializerMethodField()
    store = SerializerMethodField()

    like_btn = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    like_user_list = serializers.StringRelatedField(many=True,source='get_like_user', read_only=True)
    like_user_count = SerializerMethodField()

    # closest_like_user = serializers.SerializerMethodField()
    closest_comment = serializers.SerializerMethodField()
    load_comment_view_btn = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'url',
            'menu_url',

            #model property
            'pk',
            'store',
            'menu',
            'profile',
            'image',
            'text',
            'grade',
            'updated_at',

            # like information
            'like_btn',
            'like_status',
            'like_user_list',
            'like_user_count',

            # show thumbnail of review comment and like
            # 'closest_like_user',
            'closest_comment',

            # comment view loading
            'load_comment_view_btn'
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_at'
        ]

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_menu_url(self, obj):
        return obj.get_absolute_menu_url()

    def get_menu(self,obj):
        return obj.menu.name

    def get_profile(self,obj):
        return obj.profile.user.username

    def get_store(self,obj):
        return obj.menu.store.name

    # like serializerMethods
    def get_like_btn(self, obj):
        return reverse_lazy('api-menus:like-review', kwargs={'review_pk': obj.pk})

    def get_like_status(self, obj):
        request = self.context.get('__request')
        print(request)
        obj_profile = request.user.profile
        print(obj_profile)
        if obj_profile in obj.like_user.all():
            return True
        return False

    def get_like_user_count(self, obj):
        return obj.like_user.count()

    def get_closest_comment(self, obj):
        return obj.review_comment.first()

    # def get_closest_like_user(self, obj):
    #     request = self.context.get('__request')
    #     print('get_closest_like_user Stage 1:   ')
    #     print(self)
    #     print(type(self))
    #     like_qs = self.like_user.all()
    #     my_follow = request.following
    #     for profile in like_qs:
    #         if profile in my_follow:
    #             like_qs = [profile]
    #     return like_qs.first()

    def get_load_comment_view_btn(self, obj):
        return reverse_lazy('api-menus:review-comment-list-create', kwargs={'review_pk': obj.pk})


class UserFeedReviewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    menu = SerializerMethodField()
    profile = SerializerMethodField()
    store = SerializerMethodField()
    like_user = serializers.StringRelatedField(many=True,source='get_like_user',read_only=True)
    like_user_count = SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'pk',
            'store',
            'menu',
            'profile',
            'image',
            'text',
            'like_user',
            'like_user_count'
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_at'
        ]

    def get_menu(self,obj):
        return obj.menu.name

    def get_profile(self,obj):
        return obj.profile.user.username

    def get_store(self,obj):
        return obj.menu.store.name

    def get_like_user_count(self, obj):
        return obj.like_user.count()


class SearchMenuSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'pk',
            'image',
            'name',
            'url',
            'updated_at',
        ]

        read_only_fields =[
            'pk', 
            'created_at',
            'updated_at',
        ]

    def get_url(self, obj):
        return reverse_lazy("api-menus:menu-rud", kwargs={'store_pk': obj.store.pk,'menu_pk': obj.pk})      