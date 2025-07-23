from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password1")

    def validate(self, data):
        password1 = data.get("password1")
        password = data.get("password")
        if password1 != password:
            raise serializers.ValidationError({"detail": "password is not true"})
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return super().validate(data)

    def create(self, validated_data):
        validated_data.get("password1").pop()
        return User.objects.create_user(**validated_data)


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        date["username"] = attrs.get("username")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        password1 = attrs.get("new_password")
        password2 = attrs.get("new_password2")
        if password1 != password2:
            raise serializers.ValidationError({"detail": "password does not match"})

        try:
            validate_password(password1)

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return super().validate(attrs)


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "user does not exist"})

        attrs["user"] = user
        return super().validate(attrs)
