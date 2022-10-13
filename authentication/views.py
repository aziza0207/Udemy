import jwt
import datetime
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.conf import settings
from authentication.models import User
from .serializers import LoginSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from django.core.mail import send_mail
from uuid import uuid4
from rest_framework import generics

from .serializers import RegisterSerializer, MentorRegisterSerializer


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MentorRegisterView(generics.UpdateAPIView):
    queryset = User.objects.filter(finished_registration=False, is_mentor=True)
    serializer_class = MentorRegisterSerializer


class LoginAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data.get("email"))

        except User.DoesNotExist:
            return Response(data={"detail": "Пользователь не существует."}, status=status.HTTP_401_UNAUTHORIZED)
        is_password_valid = check_password(serializer.data.get("password"),
                                           user.password)
        if not is_password_valid:
            return Response(data={"detail": "Не верный пароль."}, status=status.HTTP_403_FORBIDDEN)
        token = jwt.encode(payload={"email": user.email}, key=settings.SECRET_KEY)
        return Response(data={'token': token})


class ResetPasswordRequestView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        try:
            user = User.objects.get(email=serializer.data.get("email"))
        except User.DoesNotExist:
            return Response(data={"detail": "The user does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

        user.reset_uuid = uuid4()
        user.reset_datetime = datetime.datetime.now()
        user.save()

        send_mail(
            'Password Reset',
            f'http://127.0.0.1:8000/auth/password_reset/{user.reset_uuid}',
            'aziza test',
            [user.email],
            fail_silently=True,
        )
        return Response(data={"message": "An email with a password "
                                         "change request has been sent to your email address."})


class PasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        reset_uuid = kwargs["uuid"]
        try:
            user = self.get_queryset().filter(
                reset_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=1)
            ).get(reset_uuid=reset_uuid)
        except User.DoesNotExist:
            return Response(data={"message": "Link is not valid!"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        password = serializer.data['password1']
        password2 = serializer.data['password2']

        if password != password2:
            return Response(data={'Passwords do not match'})

        user.set_password(password)
        user.reset_uuid = None
        user.reset_datetime = None
        user.save()
        return Response({"message": "Password recovered."})
