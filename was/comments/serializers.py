from rest_framework import serializers
from .models import NoticeComment, MenuComment, ReviewComment
from rest_framework.serializers import SerializerMethodField


class NoticeCommentSerializer(serializers.ModelSerializer):
    profile = SerializerMethodField()
    notice = SerializerMethodField()

    class Meta:
        model = NoticeComment
        fields = [
            'pk',
            'profile',
            'notice',
            'text',
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_at'
        ]

    def get_profile(self,obj):
        return obj.profile.user.username

    def get_notice(self,obj):
        return obj.notice.title
   

class MenuCommentSerializer(serializers.ModelSerializer):
    profile = SerializerMethodField()
    menu = SerializerMethodField()

    class Meta:
        model = MenuComment
        fields = [
            'pk',
            'profile',
            'menu',
            'text',
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_at'

        ]

    def get_profile(self,obj):
        return obj.profile.user.username

    def get_menu(self,obj):
        return obj.menu.name


class ReviewCommentSerializer(serializers.ModelSerializer):
    profile = SerializerMethodField()    
    review = SerializerMethodField()

    class Meta:
        model = ReviewComment
        fields = [
            'pk',
            'profile',
            'review',
            'text',
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_at'

        ]

    def get_profile(self,obj):
        return obj.profile.user.username

    def get_review(self,obj):
        return obj.review.text