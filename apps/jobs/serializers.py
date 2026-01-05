from rest_framework import serializers
from .models import Job, Skill
from apps.users.models import User


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class JobEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']


class JobSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    published_by = JobEmployerSerializer(source='employer', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'location',
            'is_remote', 'salary_min', 'salary_max', 'currency',
            'experience_level', 'employment_type', 'required_skills',
            'status', 'created_at', 'published_by'
        ]
