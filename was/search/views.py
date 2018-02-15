from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import generics, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from stores.permissions import IsOwnerOrReadOnly

from customprofile.models import UserProfile
from stores.models import Store

from stores.serializers import StoreSerializer
from .serializers import SearchFilterSerializer
from menus.serializers import ReviewSerializer, MenuSerializer

from .models import SearchFilter

from common import status_code

from menus.models import Review,Menu

from random import shuffle

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SearchFilterAPIView(generics.ListAPIView):
    serializer_class = SearchFilterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        data = self.request.query_params
        data = data['q']

        return SearchFilter.objects.filter(
            Q(searchprofile__user__username__contains=data) |
            Q(searchmenu__name__contains=data) |
            Q(searchstore__name__contains=data)
        ).order_by('-updated_at')

    def get_serializer(self,*args,**kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        status_code['SEARCH_SUCCESS']['data'] = serializer_class(*args, **kwargs).data
        return Response(status_code['SEARCH_SUCCESS'])


class RecommendAPIView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = [ReviewSerializer, MenuSerializer]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = self.request.user.profile
        location = user.location_category
        food = user.food_category.split('/')

        paginator = StandardResultsSetPagination()

        review_result_data = []
        menu_result_data = []


        review_qs = Review.objects.filter(
            Q(menu__category__in=food, menu__store__locations=location)
            ) 
            
        menu_qs = Menu.objects.filter(
            Q(category__in=food, store__locations=location)
        )


        review_serializer = ReviewSerializer(review_qs,context={'__request': request}, many=True)
        review_data = review_serializer.data

        for a in review_data:
            result = {}
            result['content_type'] = 'review'
            result['data'] = a
            result['updated_at'] = result['data']['updated_at']
            review_result_data.append(result)


        menu_serializer = MenuSerializer(menu_qs,context={'__request': request}, many=True)
        menu_data = menu_serializer.data

        for a in menu_data:
            result = {}
            result['content_type'] = 'menu'
            result['data'] = a
            result['updated_at'] = result['data']['updated_at']
            menu_result_data.append(result)

        datas = review_result_data + menu_result_data

        datas = sorted(datas,key=lambda obj: obj['updated_at'], reverse=True)

        data = self.request.query_params
        data = data['q']
    
        show_count = 6
        paginator = Paginator(datas,show_count)
        
        page = paginator.page(data)

        result_pagination = []
        result = {}
        end_index = page.end_index()

        count = len(datas) // show_count

        
        if count % show_count == 0:
            pass
        else:
            count = count + 1
        if page.number < count:
            if page.number == 1:
                
                result['next'] = "http://192.168.0.10:8003/search/recommend_list/?q=" +  str(page.number + 1)
                result['prev'] = None
            else:
                print("Why??!!!!!!")
                result['next'] = "http://192.168.0.10:8003/search/recommend_list/?q=" +  str(page.number + 1)
                result['prev'] = "http://192.168.0.10:8003/search/recommend_list/?q=" +  str(page.number - 1)

        else:
            result['next'] = None
            result['prev'] = "http://192.168.0.10:8003/search/recommend_list/?q=" +  str(page.number - 1)

        result['data'] = page.object_list
        result['recommend_all_count'] =len(datas)
    
        return Response(result)
