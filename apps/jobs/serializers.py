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
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    branch_id = serializers.IntegerField(write_only=True, required=False)
    branch_name = serializers.CharField(read_only=True, source='branch.name')

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'branch_id', 'branch_name',
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
