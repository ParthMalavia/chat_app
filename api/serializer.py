from rest_framework_simplejwt.tokens import Token
from .models import User, Profile, ChatMessage
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "full_name", "image"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)

        token["full_name"] = user.profile.full_name
        token["username"] = user.username
        token["email"] = user.email
        token["bio"] = user.profile.bio
        token["image"] = str(user.profile.image)
        token["verified"] = user.profile.verified

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[])
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2", "full_name"]

    def validate(self, attr):
        if attr["password"] != attr["password2"]:
            raise serializers.ValidationError(
                {"password": "password field does not match"})
        if not (attr.get("full_name") and attr["full_name"].strip()):
            raise serializers.ValidationError(
                {"full_name": "full_name field is required"}
            )
        else:
            attr["full_name"] = attr["full_name"].strip()
        return attr

    def create(self, attr):
        user = User.objects.create(
            username=attr['username'],
            email=attr['email'],
        )
        user.set_password(attr['password'])
        user.save()
        profile = Profile.objects.filter(user=user).first()
        if profile:
            profile.full_name = attr['full_name']
            profile.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender_profile = ProfileSerializer(read_only=True)
    receiver_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "user", "sender", "sender_profile",
                  "receiver", "receiver_profile", "message", "is_read", "date"]
