from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from comments.models import ReviewComment, NoticeComment, MenuComment
from comments.serializers import ReviewCommentSerializer, NoticeCommentSerializer, MenuCommentSerializer

from menus.models import Review, Menu
from menus.serializers import ReviewSerializer, MenuSerializer

from stores.models import Notice
from stores.serializers import NoticeSerializer

from .models import StoreFeed


class StoreFeedObjectRelatedField(serializers.RelatedField):
    
    def to_representation(self, value):
        request = self.context.get('__request')

        if isinstance(value, Notice):
            serializer = NoticeSerializer(value, context={'__request': request})
            print(serializer)
        elif isinstance(value, Menu):
            serializer = MenuSerializer(value, context={'__request': request})
            print(serializer)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class StoreFeedSerializer(serializers.ModelSerializer):
    storefeed_object = StoreFeedObjectRelatedField(read_only=True)
    store = SerializerMethodField()
    content_type = SerializerMethodField()
    shopkeeper = SerializerMethodField()


    class Meta:
        model = StoreFeed
        fields = ( 'shopkeeper','store','content_type', 'storefeed_object','updated_at')
        
        read_only_fields = [
            'pk',
            'updated_at'
        ]
    
    def get_store(self,obj):
        print('StoreFeedSerializer Stage 1: request finding...')
        request = self.context.get('__request')
        print(request)
        return obj.store.name

    def get_shopkeeper(self, obj):
        return obj.store.shopkeeper.username

    def get_content_type(self,obj):
        return obj.content_type.name

