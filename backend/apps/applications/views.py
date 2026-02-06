from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import action

from apps.core.permissions import IsEmployer, IsJobSeeker

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer, ApplicationReviewSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = serializer.validated_data['job']
        if Application.objects.filter(job=job, candidate=request.user).exists():
            return Response(
                {'message': 'Application already exists.',
                    'status_code': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(candidate=request.user)
        return Response(
            {'message': 'Application sent!', 'status_code': status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {'message': 'Applications cannot be updated once submitted.',
                'status_code': status.HTTP_403_FORBIDDEN},
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'message': "Applications cannot be updated once submitted",
                'status_code': status.HTTP_403_FORBIDDEN},
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Application deleted.'},
            status=status.HTTP_200_OK
        )


class ApplicationReviewView(APIView):
    permission_classes = (IsEmployer,)

    def patch(self, request, id):
        try:
            application = get_object_or_404(Application, id=id)
            
            if application.job.employer != request.user:
                raise Application.DoesNotExist
            
            serializer = ApplicationReviewSerializer(application, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(reviewed_at=timezone.now())
            return Response(
                {'message': 'Application reviewed successfully.',
                    'status_code': status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
        except Application.DoesNotExist:
            return Response({'message': "Application not found", 'status_code':  status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
