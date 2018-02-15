from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .models import SearchFilter

from stores.models import Store
from menus.models import Menu
from customprofile.models import UserProfile

from stores.serializers import SearchStoreSerializer
from customprofile.serializers import SearchUserProfileSerializer
from menus.serializers import SearchMenuSerializer


class SearchFilterObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Store):
            serializer = SearchStoreSerializer(value)
        elif isinstance(value, UserProfile):
            serializer = SearchUserProfileSerializer(value)
        elif isinstance(value, Menu):
            serializer = SearchMenuSerializer(value)
        else:
            raise Exception("Unexpected type of tagged object")
        return serializer.data


class SearchFilterSerializer(serializers.ModelSerializer):
    searchfilter_object = SearchFilterObjectRelatedField(read_only=True)
    content_type = SerializerMethodField()

    class Meta:
        model = SearchFilter

        fields = [
            'content_type', 'searchfilter_object', 'updated_at'
        ]
    
    def get_content_type(self, obj):
        return obj.content_type.name