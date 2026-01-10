from rest_framework import serializers
from apps.core.models import Location

class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    data = serializers.JSONField(required=False, allow_null=True)
    status_code = serializers.IntegerField()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'city', 'state', 'country', 'coordinates')
        read_only_fields = ('id',)