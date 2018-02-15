from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated # 권한과 관련된 클래스 중에서, 모든 인원에 대한 권한을 허락하는 AllowAny를 import 한다.
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer
from .renderers import UserJSONRenderer

import requests
import json

from .models import User
from .models1 import CustomprofileUserprofile
from common import status_code


class RegistrationAPIView(APIView):
    '''
    RegistrationAPIView는 등록과 관련된 APIView 인데,
    모든 인원이 접근할 수 있고,
    post 요청이 들어왔을 시에, request dict로 부터 'user' 에 관한 value 값을 변수 user에 저장한다.
    그리고 나서, RegistrationSerializer를 통해서 user를 serializer 하고,
    유효한지 확인한 이후에,
    .save()를 통해서, 저장한다.
    저장된 serializer를 serializer.data의 형태로 201_created 상태 메세지와 함께 리턴한다.

    1. 클라이언트로부터 user 데이터를 받아온다.
    2. 이 user 데이터는 serializer 과정을 꼭 거쳐야만 한다.
    3. serializer를 어떤 것을 쓸 것인가는 serialzier_class에서 지정한 것으로 하여서, user 데이터를 넘겨준다.
    4. .is_valid(raise_exception=True) 메쏘드를 사용한다.
    5. serializer가 유효하면 serializer.save()를 한다.
    6. 최종적으로 serializer.data를 리턴해 준다.

    '''
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user',{})
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True) == False:
            return Response(status_code['REGISTER_FAILURE'])    
        
        serializer.save()
        status_code['REGISTER_SUCCESS']['data'] = serializer.data

        return Response(status_code['REGISTER_SUCCESS'], status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user',{})
        try:
            login_user = User.objects.get(email=user['email'])
            user['user_id'] = login_user.pk

            if login_user.login_count != 0:
                user['profile_id'] = CustomprofileUserprofile.objects.get(user=login_user.pk).pk
            else:
                user['profile_id'] = 0

            serializer = self.serializer_class(data=user)

            if serializer.is_valid():
                data = serializer.data

                headers = {'Authorization' : 'Token ' + data['token']}
                response = requests.get("http://127.0.0.1:8002/token/save/",headers = headers)
                msg = json.loads(response.text)
                print("이것은 data 입니다.: {}".format(data))

                if response.status_code == 200 and msg['code'] == 1030:
                    login_user.login_count += 1
                    login_user.save()
                    data['login_count'] = login_user.login_count

                    status_code['LOGIN_SUCCESS']['data'] = data

                    return Response(status_code['LOGIN_SUCCESS'], status=status.HTTP_200_OK)

            else:
                return Response(status_code['LOGIN_FAILURE'])
        except:
            return Response(status_code['LOGIN_FAILURE'])


class LogoutAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        header_token = request.META['HTTP_AUTHORIZATION']
        token = header_token.split(" ")[1]
        payload = {'token':token}
        response = requests.post("http://127.0.0.1:8002/token/expiration/",data=payload)

        msg = json.loads(response.text)
        print(msg['code'])

        if response.status_code == 200 and msg['code']==1051:
            return Response(status_code['LOGOUT_SUCCESS'])
        else:
            return Response(status_code['LOGOUT_FAILURE'])