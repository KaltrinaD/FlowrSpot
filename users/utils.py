# For getting the username from the JWT token.
import jwt
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.templatetags.rest_framework import data
from core import settings
from rest_framework_simplejwt.state import token_backend


def get_auth0_user_id_from_request(request):
    authorization_heaader = request.headers.get('Authorization')

    try:
        access_token = authorization_heaader.split(' ')[1]
        print(access_token)
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('access_token expired')

    except IndexError:
        raise AuthenticationFailed('Token prefix missing')
        # token = request.COOKIES.get('jwt')
    # print(token)
    # if not token:
    #     raise AuthenticationFailed('Unauthenticated!')
    # try:
    #     payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    # except jwt.ExpiredSignatureError:
    #     raise AuthenticationFailed('Unauthenticated!')
    # # payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    # print("from getauthuser" + str(payload.get('id')))
    return payload['user_id']



