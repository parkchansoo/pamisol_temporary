# from rest_framework import status
# from rest_framework.permissions import AllowAny,IsAuthenticated # 권한과 관련된 클래스 중에서, 모든 인원에 대한 권한을 허락하는 AllowAny를 import 한다.
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .serializers import LoginSerializer, RegistrationSerializer
# from .renderers import UserJSONRenderer

# import requests


# class RegistrationAPIView(APIView):
#     '''
#     RegistrationAPIView는 등록과 관련된 APIView 인데,
#     모든 인원이 접근할 수 있고,
#     post 요청이 들어왔을 시에, request dict로 부터 'user' 에 관한 value 값을 변수 user에 저장한다.
#     그리고 나서, RegistrationSerializer를 통해서 user를 serializer 하고,
#     유효한지 확인한 이후에,
#     .save()를 통해서, 저장한다.
#     저장된 serializer를 serializer.data의 형태로 201_created 상태 메세지와 함께 리턴한다.
#     '''
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer

#     def post(self, request):
#         user = request.data.get('user',{})
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer

#     def post(self, request):
#         user = request.data.get('user',{})
#         serializer = self.serializer_class(data=user)
#         if serializer.is_valid():
#             data = serializer.data
        
#         headers = {'Authorization' : 'jwt ' + data['token']}
#         site = requests.get("http://127.0.0.1:8002/token/save/",headers = headers)

#         if site.status_code == 200:
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
