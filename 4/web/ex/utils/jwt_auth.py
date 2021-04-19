import datetime
from django.conf import settings
import jwt


def create_token(payload, timeout=2 * 60):
    salt = settings.SECRET_KEY
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers)
    return token


def get_user_id(token):
    salt = settings.SECRET_KEY
    return jwt.decode(token, salt, algorithms=['HS256'])['id']

    # encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    # print(token)
    # return jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])

    # salt = settings.SECRET_KEY
    # timeout=2 * 60
    # headers = {
    #     'typ': 'jwt',
    #     'alg': 'HS256'
    # }
    # payload = {'id': "admin1","username": "admin1"}
    # payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    # token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers)
    # print(token)
    # return jwt.decode(token, salt, algorithms=["HS256"])["id"]
    # return token
