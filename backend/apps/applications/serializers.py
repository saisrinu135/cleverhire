from rest_framework import serializers
from apps.applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'job', 'candidate', 'cover_letter', 'resume_snapshot', 'match_score', 'status', 'applied_at', 'reviewed_at')  # Fixed typo: 'fileds' -> 'fields'
        read_only_fields = ('id', 'candidate', 'match_score', 'status', 'applied_at', 'reviewed_at')


class ApplicationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'status', 'reviewed_at')
        read_only_fields = ('id', 'reviewed_at')
    
    def validate_status(self, value):
        if value not in dict(Application.Status.choices):
            raise serializers.ValidationError("Invalid status.")
        return value