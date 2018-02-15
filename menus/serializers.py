from rest_framework import serializers
from .models import Menu, Review



class MenuSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Menu
        fields = [
            'pk',
            'name',
            'description',
            'price',
            'store',
        ]

        read_only_fields = [
            'store', 'pk',
        ]



class ReviewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Review
        fields = [
            'pk',
            'text',
            'user',
            'menu',
            # image
            # like
            # hit
            # grade
        ]

        read_only_fields = [
            'pk', 'user', 'menu'
        ]