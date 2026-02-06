from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response


from apps.core.models import Location
from apps.core.serializers import LocationSerializer


class LocationsView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]


class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUser]


def custom404(request, exception=None):
    return JsonResponse({
        'success': False,
        'message': 'Not Found',
        'errors': 'The requested resource was not found.',
        'status_code': 404
    }, status=404)


def custom500(request):
    return JsonResponse({
        'success': False,
        'message': 'Internal Server Error',
        'errors': 'Something went wrong. Please try again later.',
        'status_code': 500
    }, status=500)
