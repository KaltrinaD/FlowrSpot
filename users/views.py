from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from core import settings
from .serializers import UserSerializer, FlowerSerializer, SightingSerializer,  \
    TokenObtainPairPatchedSerializer, CustomTokenRefreshSerializer, SightingLikesSerializer
from .models import User, Flowers, SightingModel, SightingLikes
import jwt
from .utils import get_auth0_user_id_from_request
from .get_qod import get_quota
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        authorization_heaader = request.headers.get('Authorization')

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        try:
            access_token = authorization_heaader.split(' ')[1]
            print(access_token)
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('access_token expired')

        except IndexError:
            raise AuthenticationFailed('Token prefix missing')

        if user.id != payload['user_id']:
            return Response ("Bad Request")

        response = Response()

        response.set_cookie(key='jwt', value=access_token)
        response.data = {
            'jwt': access_token
        }

        return response


class UserView(APIView):

    def get(self, request):
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

        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class FlowerView(APIView):
    def get(self, request):
        flowers = Flowers.objects.all()
        flowers_serializer = FlowerSerializer(flowers, many=True)
        return Response(flowers_serializer.data)


class FlowerViewByIdView(APIView):

    def get_object(self, id):
        try:
            return Flowers.objects.get(id=id)
        except Flowers.DoesNotExist as e:
            return Response({"error": "Not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        flowers=SightingModel.objects.filter(flower_id=id)
        flowers_serializer = SightingSerializer(flowers, many=True)
        return Response(flowers_serializer.data)


class TokenObtainPairPatchedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairPatchedSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Refresh token View
    """

    serializer_class = CustomTokenRefreshSerializer


class SightingView(APIView):

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)

    def get(self, request):
        sightings = SightingModel.objects.all()
        flowers_serializer = SightingSerializer(sightings, many=True)
        return Response(flowers_serializer.data)

    def post(self, request):
        sightingsserializer = SightingSerializer(data=request.data)
        auth0_user_id = get_auth0_user_id_from_request(self.request)
        print(auth0_user_id)
        auth0_user_id = User.objects.filter(id=auth0_user_id).first()
        print('authuserid '+ str(auth0_user_id))
        if sightingsserializer.is_valid():
            sightingsserializer.save(quote=get_quota(self), created_by=auth0_user_id)
            print(request.data['user'])
            return Response(sightingsserializer.data, status=status.HTTP_201_CREATED)
        return Response(sightingsserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SightingByIdView(APIView):

    def get_object(self, id):
        try:
            return SightingModel.objects.get(sighting_id=id)
        except SightingModel.DoesNotExist as e:
            return Response({"error": "Not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = SightingSerializer(instance)
        return Response(serializer.data)

    def delete(self, request, id):
        instance = self.get_object(id)
        serializer = SightingSerializer(instance)
        auth0_user_id = get_auth0_user_id_from_request(self.request)
        auth0_user_id = User.objects.filter(id=auth0_user_id).first()
        print(auth0_user_id)
        user_sight = SightingModel.objects.filter(sighting_id=id).first()
        print(user_sight.created_by)
        if str(auth0_user_id) == str(user_sight.created_by):
            print(auth0_user_id)
            instance.delete()
            return Response(serializer.data)
        return Response("user not authorized")


class LikesSightingView(APIView):
        def get(self, request, format=None):
            content = {
                'status': 'request was permitted'
            }
            return Response(content)

        def get(self, request):
            likes = SightingLikes.objects.all()
            serializer = SightingLikesSerializer(likes, many=True)
            return Response(serializer.data)

        def post(self, request):
            serializer = SightingLikesSerializer(data=request.data)
            auth0_user_id = get_auth0_user_id_from_request(self.request)
            auth0_user_id = User.objects.filter(id=auth0_user_id).first()
            print(auth0_user_id)
            if serializer.is_valid():
                serializer.save(created_by=auth0_user_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikesSightingLViewById(APIView):

        def get_object(self, id):
            try:
                return SightingLikes.objects.get(id=id)
            except SightingLikes.DoesNotExist as e:
                return Response({"error": "Not found."}, status=404)

        def get(self, request, id=None):
            instance = self.get_object(id)
            serializer = SightingLikesSerializer(instance)
            return Response(serializer.data)

        def patch(self, request, id, format=None):
            transformer = self.get_object(id)
            serializer = SightingLikesSerializer(transformer,
                                         data=request.data,
                                         partial=True)
            auth0_user_id = get_auth0_user_id_from_request(self.request)
            auth0_user_id = User.objects.filter(id=auth0_user_id).first()
            print(auth0_user_id)
            user_like =SightingLikes.objects.filter(id=id).first()
            print(user_like.created_by)
            if str(auth0_user_id) == str(user_like.created_by):
                if serializer.is_valid():
                    serializer.save(source=auth0_user_id)
                    return Response(serializer.data)
            return Response("Bad Request")
