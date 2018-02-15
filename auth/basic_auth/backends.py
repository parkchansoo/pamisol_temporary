import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        print("JWTAuthentication Class -- IN ")
        print("auth_header : {}".format(auth_header)) # Token을 헤더에 싣지 않으면 아무값도 없고, 헤더에 실었을 시에는 Header에 실은 Token 값을 보여준다.
        '''
        [b'Token', b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTcsImV4cCI6MTUxNzkwNDA2MH0.GJeHV4hyGoR8XiFqfx1XpJjVs53NkNAEYRqoUvjYBy8']
        '''
        print("auth_header_prefix : {}".format(auth_header_prefix))

# 여기를 기준으로 만약 아래 조건이 충족하면, None을 리턴하고, -> 로그인 시,
# 아래 조건을 충족하지 않는다면, if 문 이하를 실행한다. -> api server 호출 시 혹은 로그아웃 시
        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None 

        elif len(auth_header) > 2:
            return None


        #auth_header[0] or [1] 부분은 byte 타입이므로, decode('utf-8)을 이용해서, str 형태로 만들어준다.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        print("before prefix : {}".format(auth_header[0]))
        print("before token : {}".format(auth_header[1]))
        print("before prefix : {}".format(type(auth_header[0])))
        print("\n")
        print("decoded prefix : {}".format(prefix))
        print("decoded token : {}".format(token))
        print("decoded prefix : {}".format(type(prefix)))

        #앞에 prefix를 확인한다.
        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    #여기선 총 3가지를 확인한다.
    '''
    1. 받은 jwt token을 decode 할 수 있는지를 확인한다.
    2. token을 decode 했을 때, 얻는 id 값으로 실제 유저가 존재하는지를 확인한다.
    3. user가 active 한 유저인지 확인한다.
    '''
    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except:
            msg = "Invalid authentication. Could not decode token"
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found'
            raise exceptions.AuthenticationFailed(msg)
        
        if not user.is_active:
            msg = 'This user has been deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)