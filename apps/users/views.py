import uuid

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model, authenticate

from apps.core.serializers import ResponseSerializer
from apps.core.permissions import IsEmployer

from apps.users.serializers import (
    SignUpSerializer, UserSerializer, LoginRequestSerializer, LogoutRequestSerializer, UserVerifyRequest,
    CompanySerializer
)
from apps.users.utils import generate_verification_token, verify_token
from apps.users.models import CompanyProfile
from apps.users import tasks

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.email_token = generate_verification_token(user.id)
        user.save()

        # Send verification email
        tasks.send_verification_email.delay_on_commit(user.id)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginRequestSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if not user:
            raise AuthenticationFailed(detail='Invalid credentials')

        if not user.is_active:
            raise AuthenticationFailed(detail='User account is disabled.')

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutRequestSerializer

    def post(self, request):
        serializer = LogoutRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        refresh_token = serializer.validated_data.get('refresh')
        if not refresh_token:
            raise AuthenticationFailed(detail='Invalid refresh token')

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            response_serializer = ResponseSerializer(data={
                'status_code': status.HTTP_200_OK,
                'message': 'Logout successful',
                "status": True
            })

            response_serializer.is_valid(raise_exception=True)

            return Response(response_serializer.validated_data)

        except TokenError:
            raise AuthenticationFailed(detail='Invalid token')


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserVerify(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserVerifyRequest

    def post(self, requst):
        serializer = self.serializer_class(data=requst.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        token = serializer.validated_data.get('token')
        if not token:
            raise AuthenticationFailed(detail='Invalid token')
        try:
            user_id = verify_token(token)
            user = User.objects.get(id=user_id)
            user.is_email_verified = True
            user.email_token = None
            user.save()
            return Response({
                'status_code': status.HTTP_200_OK,
                'message': 'Email verified successfully',
                "status": True
            })
        except User.DoesNotExist:
            raise AuthenticationFailed(detail='Invalid token')


class ResendVerificationEmail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request):
        try:
            user = self.get_object()

            if user.is_email_verified:
                raise ValidationError('Email already verified')

            user.email_token = generate_verification_token(user.id)
            user.save()

            return Response(data={
                "success": True,
                "message": "Verification email sent successfully",
                "status_code": 200
            }, status=status.HTTP_201_CREATED
            )
        except User.DoesNotExist:
            raise AuthenticationFailed(detail='User not found')


class CompanyView(generics.ListCreateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        existing_company = CompanyProfile.objects.filter(company_name=serializer.validated_data.get('company_name')).exists()
        if existing_company:
            raise ValidationError('Company already exists')
        
        serializer.save(user=self.request.user)
