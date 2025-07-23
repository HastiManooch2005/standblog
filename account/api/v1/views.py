from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializer import (
    RegisterSerializer,
    TokenObtainPairSerializer,
    ChangePasswordSerializer,
    ActivationSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import send_mail as send_templated_mail
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import JWTError, ExpiredSignatureError, InvalidToken


class UserRegistrationView(GenericAPIView):  #
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            serializer.save()

            data = {
                "email": serializer.validated_data["email"],
            }
            user_object = User.objects.get(email=serializer.validated_data["email"])
            token = RefreshToken.for_user(user_object)
            send_templated_mail(
                "hello.tpl",  # مسیر تمپلیت
                {"token": Token},  # context داده‌ها
                "from@example.com",  # ایمیل فرستنده
                ["hastimanooch84@gmail.com"],  # لیست گیرندگان
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            if not user.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user.set_password(serializer.data.get("new_password"))
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMail(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        self.email = "hastimanooch84@gmail.com"
        user_object = User.objects.get(email=self.email)
        token = RefreshToken.for_user(user_object)
        try:

            send_templated_mail(
                "hello.tpl",  # مسیر تمپلیت
                {"token": Token},  # context داده‌ها
                "from@example.com",  # ایمیل فرستنده
                ["hastimanooch84@gmail.com"],  # لیست گیرندگان
            )
            return Response({"message": "Email sent successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationView(APIView):
    def get(self, token, request, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response({"error": "Activation link is expired."}, status=401)
        except InvalidTokenError:
            user_id = token.get("user_id")
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()


class ActivationResendView(APIView):

    def post(self, request, *args, **kwargs):
        serializer_class = ActivationSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.validated_data["user"]
        token = RefreshToken.for_user(user)
        send_templated_mail(
            "activationcode.tpl",  # مسیر تمپلیت
            {"token": Token},  # context داده‌ها
            "from@example.com",  # ایمیل فرستنده
            [user.email],  # لیست گیرندگان
        )
        return Response({"message": "Email sent successfully!"})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
