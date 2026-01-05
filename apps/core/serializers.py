from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    data = serializers.JSONField(required=False, allow_null=True)
    status_code = serializers.IntegerField()