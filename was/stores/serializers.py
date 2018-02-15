from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.urls import reverse_lazy
from stores.models import Store, Notice


class NoticeThumbnailSerializer(serializers.ModelSerializer):
    title_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields =[
            'pk',
            'title_thumbnail',
        ]

        read_only_fields = [
            'pk',
        ]

    def get_title_thumbnail(self, obj):
        title = obj.title
        if len(title) > 22:
            title = title[:22] + '...'
        return title


class StoreSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    notice_url = serializers.SerializerMethodField()
    follow_btn = serializers.SerializerMethodField()
    follow_status = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = [
            'pk',
            'image',
            'shopkeeper',
            'name',
            'locations',
            'phone',
            'description',

            'follow_btn',
            'follow_status',

            # notice parts
            'notice_url',
            'updated_at',
        ]

        read_only_fields =[
            'pk',
            'created_at',
            'updated_at',
        ]

    def get_notice_url(self, obj):
        return reverse_lazy('api-stores:notice-create-list', kwargs={'store_pk': obj.pk})

    def get_follow_btn(self, obj):
        return reverse_lazy('api-stores:store-follow', kwargs={'store_pk': obj.pk})

    def get_follow_status(self, obj):
        request = self.context.get('__request')
        if obj in request.user.profile.get_store_following():
            return True
        return False


class SearchStoreSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Store
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
        return reverse_lazy("api-stores:store-detial", kwargs={'store_pk': obj.pk})


class NoticeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    like_btn = serializers.SerializerMethodField()
    like_user = serializers.StringRelatedField(many=True,source='get_like_user',read_only=True)
    like_user_count = SerializerMethodField()

    class Meta:
        model = Notice
        fields =[
            'like_btn',
            'pk',
            'image',
            'title',
            'text',
            'like_user',
            'like_user_count',
            'hit',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_NoticeSerializerat',
        ]
    def get_like_btn(self, obj):
        return reverse_lazy('api-stores:notice-like', kwargs={'notice_pk':obj.pk})

    def get_like_user_count(self, obj):
        return obj.like_user.count()

