from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.jobs.models import Job, Skill, SavedJob
from apps.jobs.serializers import JobSerializer, SkillSerializer, SavedJobSerializer

from apps.core.permissions import IsEmployer
from apps.core.pagination import VariableResultsSetPagination


User = get_user_model()


class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]
    lookup_field = 'id'

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'is_remote', 'employment_type',
                        'experience_level', 'company', 'created_at']
    ordering_fields = ['created_at', 'updated_at', 'title',
                       'salary_min', 'salary_max', 'company__company_name']
    ordering = ['-updated_at', '-created_at']
    search_fields = ['title']

    def perform_create(self, serializer):
        user = self.request.user
        company = None

        # Check if user is currently working at a company
        experience = user.experiences.filter(
            is_current=True,
            company__isnull=False
        ).first()

        if experience:
            company = experience.company

        if not company:
            raise ValidationError(
                {"company": "You must have an active employment record at a company to post a job."}
            )

        serializer.save(
            employer=user,
            company=company
        )

    def get_queryset(self):
        queryset = super().get_queryset().filter(employer=self.request.user)

        sort_by = self.request.query_params.get('sort_by', None)
        order = self.request.query_params.get('order', None)

        if sort_by and order:
            if order == 'asc':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by(f'-{sort_by}')

        return queryset


class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]
    lookup_field = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(employer=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class SkillListCreateAPIView(generics.CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class JobPublishAPIView(APIView):
    permission_classes = [IsEmployer]

    def post(self, request, id):
        try:
            job = Job.objects.get(id=id, employer=request.user)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        if job.status == Job.Status.PUBLISHED:
            return Response({"status": "Job is already published"}, status=status.HTTP_400_BAD_REQUEST)

        job.status = Job.Status.PUBLISHED
        job.save()
        return Response({"status": "Job published successfully"}, status=status.HTTP_200_OK)


class JobCloseAPIView(APIView):
    permission_classes = [IsEmployer]

    def post(self, request, id):
        try:
            job = Job.objects.get(id=id, employer=request.user)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        if job.status == Job.Status.CLOSED:
            return Response({"status": "Job is already closed"}, status=status.HTTP_400_BAD_REQUEST)

        job.status = Job.Status.CLOSED
        job.save()
        return Response({"status": "Job closed successfully"}, status=status.HTTP_200_OK)


class SkillsListView(generics.ListAPIView):
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category']
    pagination_class = VariableResultsSetPagination


class JobSaveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        job = get_object_or_404(Job.active_objects, id=id)

        saved_existing_job = SavedJob.objects.filter(user=request.user, job=job)

        if saved_existing_job:
            saved_existing_job.delete()
            return Response({'message': 'Job removed from saved', "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            saved_job = SavedJob.objects.create(user=request.user, job=job)
            return Response({'message': 'Job saved successfully', "status_code": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)