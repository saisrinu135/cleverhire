import uuid

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone

from apps.core.serializers import ResponseSerializer
from apps.core.permissions import IsEmployer

from apps.users.serializers import (
    SignUpSerializer, UserSerializer, LoginRequestSerializer, LogoutRequestSerializer, UserVerifyRequest,
    CompanySerializer, ProfileSerializer, ExperienceSerializer, EducationSerializer
)
from apps.users.utils import generate_verification_token, verify_token
from apps.users.models import CompanyProfile, Profile, Experience, Education
from apps.users import tasks

from rest_framework import viewsets

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status_code': status.HTTP_201_CREATED,
            'message': 'User registered successfully. Please check your email to verify your account.',
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


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
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': 'Login successful',
            "status": True,
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
    queryset = CompanyProfile.active_objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        existing_company = CompanyProfile.objects.filter(
            company_name=serializer.validated_data.get('company_name')).exists()
        if existing_company:
            raise ValidationError('Company already exists')

        serializer.save()


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyProfile.active_objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class PofileCreateView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        user = request.user

        if hasattr(user, 'profile'):
            raise ValidationError("Profile already exists")

        resume_file = request.FILES.get('resume')

        if resume_file:
            allowed_types = ['application/pdf']
            if resume_file.content_type not in allowed_types:
                raise ValidationError("Only PDF is accepted")
            max_size = 5 * 1024 * 1024  # 5MB
            if resume_file.size > max_size:
                raise ValidationError("File size exceeds 5MB limit")

        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        skills = serializer.validated_data.pop('skills', [])

        profile = Profile.objects.create(
            user=user,
            full_name=f"{user.first_name} {user.last_name}",
            **serializer.validated_data
        )

        profile.calculate_completeness()

        if skills:
            profile.skills.set(skills)

        if profile.resume:
            tasks.parse_resume.delay_on_commit(profile.id)

        return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class ExperienceView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_current') == True:
            serializer.validated_data['end_date'] = None
        serializer.save(user=self.request.user)


class ExperienceDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EducationView(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
