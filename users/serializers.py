from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Profile




class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        access = token_backend.decode(data['access'], verify=True)
        data['access'] = access
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        if validated_data:
            return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


    def validate(self, data):
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            return {'access': access_token, 'refresh': refresh_token, 'username': user.username}

        except CustomUser.DoesNotExist as e:
            raise serializers.ValidationError("Invalid login credentials") from e

    class Meta:
        model = CustomUser
        fields =  ('username', 'password', 'access', 'refresh')
        read_only_fields = ( 'access', 'refresh')

    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)


    class Meta:
        model = Profile 
        fields = ['id', 'user']


class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'password']
