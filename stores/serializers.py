from rest_framework import serializers
from stores.models import Store, Notice


class StoreSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Store
        fields = [
            'pk',
            'shopkeeper',
            'name',
            'locations',
            'phone',
            'description',
            'image',
            'created_at',
            'updated_at',
        ]

        read_only_fields =['pk', 'shopkeeper']


class NoticeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Notice
        fields =[
            'pk',
            'store',
            'title',
            'text',
            # 'like',
            # 'hit',
            'image',
            # 'category',
        ]

        read_only_fields = ['pk', 'store']

    # def create(self, validated_data):
    #     store = Store.objects.get(pk=self.store_id)
    #     return Notice(**validated_data)

    # def get
    '''
    this functions is to get store_pk to filter notice
    which is store-related
     
    '''