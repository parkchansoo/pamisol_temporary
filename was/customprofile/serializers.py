from django.conf import settings
from django.urls import reverse_lazy

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework import pagination

from menus.models import Review
from menus.serializers import ReviewSerializer

from basic_auth.models import User
from stores.models import Store
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # profile owner's information
    image = serializers.ImageField(use_url=True)
    user = serializers.SerializerMethodField()
    url_follow_toggle = serializers.SerializerMethodField()
    follow_status = serializers.SerializerMethodField()

    # following = serializers.StringRelatedField(many=True,source='get_following')
    following_count = SerializerMethodField()
    # store_following = serializers.StringRelatedField(many=True,source='get_store_following')
    store_following_count = SerializerMethodField()
    followed_by_count = SerializerMethodField()
    url_list_reviewer = serializers.SerializerMethodField()
    url_list_store = serializers.SerializerMethodField()
    url_list_followed = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField('paginated_reviews')
    review_count = SerializerMethodField()
    review_pagination_count = SerializerMethodField()

    class Meta:
        model = UserProfile

        fields = [
            # profile owner's information
            'pk',
            'image',
            'user',
            'description',
            'url_follow_toggle',
            'follow_status',

            # follwing list's information
            # 'following',
            'following_count',
            # "store_following",
            "store_following_count",
            'followed_by_count',
            # 'followed_by_user_list',

            'url_list_reviewer',
            'url_list_store',
            'url_list_followed',

            # archived review information on profile
            'review_count',
            'review_pagination_count',
            'reviews',
        ]

        read_only_fields = [
            'pk',
            'user',
            # 'following',
            'following_count',
            # "store_following",
            "store_following_count",

            'reviews'
        ]

    # own information
    def get_user(self, obj):
        return obj.user.email

    # provied url's method fields
    def get_url_follow_toggle(self, obj):
        print('get_follow_toggle_url functions working: ')
        return reverse_lazy("customprofile:toggle-follow", kwargs={'profile_pk': obj.pk})

    def get_url_list_reviewer(self, obj):
        return reverse_lazy("customprofile:follow-reviewer-list", kwargs={'profile_pk': obj.pk})

    def get_url_list_store(self, obj):
        return reverse_lazy("customprofile:follow-store-list", kwargs={'profile_pk': obj.pk})

    def get_url_list_followed(self, obj):
        return reverse_lazy("customprofile:followed-user-list", kwargs={'profile_pk': obj.pk})

    def get_follow_status(self, obj):
        request = self.context.get('__request')
        if obj.user in request.user.profile.following.all():
            return True
        return False

    # providing following count's
    def get_following_count(self, obj):
        return obj.following.count()

    def get_followed_by_count(self, obj):
        return obj.user.followers.count()

    def get_store_following_count(self, obj):
        return obj.store_following.count()

    def paginated_reviews(self, obj):
        print(obj)
        reviews = Review.objects.filter(profile=obj).order_by('-updated_at')
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(reviews, self.context['request'])
        print('UserProfileSerializer Stage 1: ')
        print(type(page))
        print(page)
        serializer = ReviewSerializer(page, many=True, context={'__request': self.context['request']})
        print(serializer)
        return serializer.data

    def get_review_count(self, obj):
        return Review.objects.filter(profile=obj).count()

    def get_review_pagination_count(self, obj):
        all = Review.objects.filter(profile=obj).count()

        if all % 15 == 0:
            return all / 15
        else:
            return int((all / 15) + 1)


class DefaultUserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'pk',
            # 'user',
            'image',
            'location_category',
            'food_category',
        ]

        read_only_fields = [
            'pk']


class StoreFollowingListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Store

        fields = [
            'pk',
            'name',
            'shopkeeper',
            'image',
        ]


class UserProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = UserProfile
        fields = ['image']


class ReviewerFollowingListSerializer(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            'pk',
            'username',
            'image',
        ]

    def get_pk(self, obj):
        return obj.profile.pk

    def get_image(self, obj):
        profiles = obj.profile
        serializer = UserProfileImageSerializer(profiles)
        return serializer.data['image']


class UserFollowedListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile

        fields = [
            'pk',
            'username',
            'image',
        ]
    def get_username(self, obj):
        return obj.user.username


class SearchUserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    url = serializers.SerializerMethodField()
    name = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'pk',
            'image',
            'name',
            'url',
            'updated_at',
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'updated_at',
        ]

    def get_url(self, obj):
        return reverse_lazy("customprofile:profile-detail", kwargs={'profile_pk': obj.pk})

    def get_name(self, obj):
        return obj.user.username
