from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from jwt import exceptions


class JwtQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 抛出异常
        # return一个元祖， （1,2）认证通过，在
        # None
        token = request.META.get('HTTP_AUTHORIZATION')
        salt = settings.SECRET_KEY
        verified_payload = None
        try:
            verified_payload = jwt.decode(token, salt, algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            # token已失效
            raise AuthenticationFailed({'code': 203, 'error': 'token已失效'})
        except jwt.DecodeError:
            # token认证失败
            raise AuthenticationFailed({'code': 202, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            # 非法的token
            raise AuthenticationFailed({'code': 201, 'error': '非法的token'})
        return verified_payload, token
