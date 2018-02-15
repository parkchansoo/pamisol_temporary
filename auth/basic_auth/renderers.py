import json
from rest_framework.renderers import JSONRenderer


#utf-8 인코딩을 이용해서 request data를 json으로 렌더링 한다.

class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        # data는 serializer.data를 의미한다.
        '''
        {'email': 'ueee1@test.com', 'user_id': 17, 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTc5MDIzMzAsImlkIjoxN30.Bh9FsfFU7D6JSr_yUnqwD9KPaXUdYxg9o-1Xe8UHM9E'}
        '''
        # 여끼써 media_type은 application/json이고,
        # renderer_context는 다음과 같다.

        '''
        {'view': <basic_auth.views.LoginAPIView object at 0x7f5357509a90>, 
        'response': <Response status_code=200, "application/json; charset=utf-8">, 
        'request': <rest_framework.request.Request object at 0x7f5356c94c18>, 
        'args': (), 
        'kwargs': {}}
        '''

        print(data)
        print(media_type)
        print(renderer_context)


        errors = data.get('errors', None)
        token = data.get('token', None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        k = json.dumps({'user' : data})
        print(type(k))

        return json.dumps({
            'user' : data
    })