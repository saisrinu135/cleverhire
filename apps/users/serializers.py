from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.core.serializers import ResponseSerializer, LocationSerializer
from apps.users.models import CompanyProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name',
                  'last_name', 'role', 'avatar', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'email', 'role',
                            'username', 'is_staff', 'is_superuser']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']
        read_only_fields = ['role']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.Role.JOB_SEEKER)
        )
        return user


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)


class UserVerifyRequest(serializers.Serializer):
    token = serializers.UUIDField(write_only=True)


class CompanyBasicSerializer(serializers.ModelSerializer):
    """Basic company info for nested serialization"""
    class Meta:
        model = CompanyProfile
        fields = ('id', 'company_name', 'company_size', 'industry',
                  'website', 'description', 'logo', 'founded_date')


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True, required=False)
    location_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )

    class Meta:
        model = CompanyProfile
        fields = ('id', 'user', 'company_name', 'company_size', 'industry',
                  'website', 'description', 'logo', 'founded_date', 'locations', 'location_ids')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        location_ids = validated_data.pop('location_ids', [])
        user = self.context['request'].user

        company = CompanyProfile.objects.create(user=user, **validated_data)

        if location_ids:
            company.locations.set(location_ids)

        return company
    

    def update(self, instance, validated_data):
        location_ids = validated_data.pop('location_ids', [])
        instance = super().update(instance, validated_data)
        if location_ids is not None:
            instance.locations.set(location_ids)
        return instance
