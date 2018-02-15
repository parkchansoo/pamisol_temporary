from django.db.models import Q

from rest_framework import generics, permissions

from stores.permissions import IsOwnerOrReadOnly

from customprofile.models import UserProfile
from stores.models import Notice
from menus.models import Review, Menu
from comments.models import ReviewComment, NoticeComment, MenuComment

from menus.serializers import UserFeedReviewSerializer, MenuSerializer, ReviewSerializer
from comments.serializers import ReviewCommentSerializer, NoticeCommentSerializer, MenuCommentSerializer
from stores.serializers import NoticeSerializer
from .serializers import StoreFeedSerializer
from .models import StoreFeed


class UserFeedsAPIView(generics.ListCreateAPIView):
    lookup_url_kwargs = 'profile_pk'
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        profile_pk = self.kwargs['profile_pk']
        following = UserProfile.objects.get(pk=profile_pk).following.all()

        result = set()

        first = Review.objects.filter(profile__user__in=following)

        for review in first:
            result.add(review)

        for user in following:
            for review in user.profile.review_like.all():
                result.add(review)

        result = list(result)

        if len(result) < 6:
            user_profile = UserProfile.objects.get(pk=profile_pk)
            food = user_profile.food_category.split("/")
            location = user_profile.location_category

            result_pk = [review.pk for review in result]

            cnt = 6 - len(result)
            random_review = Review.objects.exclude(pk__in=result_pk).order_by("-updated_at")[:cnt]
 
            cnt=0
            for review in random_review:
                result.append(review)
                cnt += 1
                if cnt == len(random_review):
                    break

        return sorted(result,key=lambda obj: obj.updated_at, reverse=True)

    def get_serializer_context(self, *args, **kwargs):
        context = super(UserFeedsAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context    


class StoreFeedsAPIView(generics.ListCreateAPIView):
    lookup_url_kwargs = 'profile_pk'
    serializer_class = StoreFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        profile_pk = self.kwargs['profile_pk']        
        store_following = UserProfile.objects.get(pk=profile_pk).store_following.all()
        return StoreFeed.objects.filter(store__in=store_following).order_by('-updated_at')

    # put request in context so that serializer can get request.user
    def get_serializer_context(self, *args, **kwargs):
        context = super(StoreFeedsAPIView, self).get_serializer_context(*args, **kwargs)
        context['__request'] = self.request
        return context