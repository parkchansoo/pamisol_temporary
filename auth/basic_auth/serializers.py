from django.contrib.auth import authenticate

from rest_framework.serializers import ModelSerializer,Serializer,CharField,ValidationError,IntegerField

from .models import User


class RegistrationSerializer(ModelSerializer):
    '''
    RegistrationSerializer는 email, username, password와 token에 대해서 직렬화를 해준다.
    해당 클래스는 ModelSeirlaizer 클래스에서 create method를 오버라이딩 하였고, 이 method는
    validated 된 dict 데이터를 받아서, user를 생성하여 리턴한다.

    '''
    password = CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_shopkeeper']

        
    def create(self, validated_data):
        print("RegistrationSerializer -- post mehtod -- IN")
        print("created 메쏘드의 self: {}".format(self))
        print("created 메쏘드의 validated_data: {}".format(validated_data))

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_shopkeeper=validated_data['is_shopkeeper'])

        user.set_password(validated_data['password'])
        user.save()
        print("RegistrationSerializer -- post mehtod -- OUT")
        return user


class LoginSerializer(Serializer):
    user_id = IntegerField()
    profile_id = IntegerField()
    email = CharField(max_length=255)
    password = CharField(max_length=128, write_only=True)
    token = CharField(max_length=255, read_only=True)


    def validate(self, data):
        '''
        validate 메쏘드는 Loginserializer가 valid 한지를 확인하는 것 이다.
        이것이 패스하면, email, password가 매칭 된다는 것을 말한다.
        '''

        email = data.get('email',None)
        password = data.get('password',None)
        user_id = data.get('user_id',None)
        profile_id = data.get('profile_id',None)

        
        if email is None:
            raise ValidationError(
                'An email address is required to log in.'
            )
        
        if password is None:
            raise ValidationError(
                'A password is required to log in.'
            )

        '''
        authenticate 메쏘드는 email과 password가 매칭하는지를 확인한다.
        '''
        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError(
                'A user with this email and password was not found.'
            )
        
        if not user.is_active:
            raise ValidationError(
                'This user has been deactivated.'
            )

        #user['user_id'] = pk



        return {
            'token':user.token,
            'email':user.email,
            'user_id':user_id,
            'profile_id':profile_id,
            
            }