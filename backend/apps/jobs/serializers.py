from rest_framework import serializers
from apps.core.serializers import LocationSerializer
from apps.core.models import Location
from apps.jobs.models import Job, Skill, SavedJob
from apps.users.models import User, CompanyProfile


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class JobEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']


class JobCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['id', 'company_name', 'logo']


class JobSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    published_by = JobEmployerSerializer(source='employer', read_only=True)
    company = JobCompanySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True, required=False
    )
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description','company', 'location', 'location_id',
            'is_remote', 'salary_min', 'salary_max', 'currency',
            'experience_level', 'employment_type', 'required_skills',
            'status', 'created_at', 'published_by', 'skill_ids', 'application_count', 'view_count'
        ]

    def create(self, validated_data):
        skill_ids = validated_data.pop('skill_ids', [])
        job = Job.objects.create(**validated_data)
        if skill_ids:
            job.required_skills.set(skill_ids)
        return job

    def update(self, instance, validated_data):
        skill_ids = validated_data.pop('skill_ids', None)
        if skill_ids is not None:
            instance.required_skills.set(skill_ids)

        return super().update(instance, validated_data)


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'user']