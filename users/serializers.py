import datetime

from django.db.models import UniqueConstraint
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User, Flowers, SightingModel, SightingLikes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowers
        fields = ['id', 'name', 'image', 'description']


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingModel
        fields = ['flower_id', 'longitude', 'latitude', 'created', 'updated', 'image', 'user']
        user = serializers.ReadOnlyField(source=User.id)
        created_by = serializers.ReadOnlyField(source=User.id)
        extra_kwargs = {
            'created_by': {'read_only': True}
        }


class SightingLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingLikes
        unique_together = (('created_by', 'sight'),)
        fields = ['like', 'user',  'created_by', 'sight']
        created_by = serializers.ReadOnlyField(source=User.id)
        extra_kwargs = {
            'created_by': {'read_only': True}
        }


class TokenObtainPairPatchedSerializer(TokenObtainPairSerializer):
    def to_representation(self, instance):
        r = super(TokenObtainPairPatchedSerializer, self).to_representation(instance)
        r.update({'user': self.User.id})
        return r




class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        #     'iat': datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid=decoded_payload['user_id']
        # response.set_cookie(key='jwt', value=token)
        # add filter query
        data.update({'user': user_uid})
        return data

