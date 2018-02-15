import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

class UserManager(BaseUserManager):
    """
    장고에서 custom user를 설정하려면, UserManager를 통해서 해야한다.
    'BaseUserManager'를 상속받으면, 이것으로 부터, User를 생성할 때 쓰는 코드들을 얻을 수 있다.
    User 객체를 생성하기위해서, 우리는 'crate_user'를 오버라이드 해서 사용할 수 있다.
    """

    def create_user(self, username, email, password=None):
        """
        기본적으로 username, email, password를 입력 받는다.
        username, email 모두 있어야한다.
        """

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    
    def create_superuser(self, username, email, password):
        """
        superuser도 생성하는 법은 마찬가지인데,
        권한에 대한 수정이 추가로 있다.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_shopkeeper = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    login_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #USERNAME_FIELD는 로그인 할 때, 어떤 필드로 할거냐를 정하는 변수이다.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(minutes=60)
        token = jwt.encode({
            'id' : self.pk,
            'exp' : int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

