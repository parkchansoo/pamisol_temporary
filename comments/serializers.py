from rest_framework import serializers
from .models import NoticeComment, MenuComment, ReviewComment


class NoticeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoticeComment
        fields = [
            'pk',
            'text',
            'user',
            'notice',
            'like',
        ]

        read_only_fields = [
            'pk', 'notice', 'like', 'user',
        ]


class MenuCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuComment
        fields = [
            'pk',
            'text',
            'user',
            'menu',
            'like',
        ]

        read_only_fields = [
            'pk', 'menu', 'like', 'user',
        ]


class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = [
            'pk',
            'text',
            'user',
            'review',
            'like',
        ]

        read_only_fields = [
            'pk', 'review', 'like', 'user',
        ]