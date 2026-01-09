from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.jobs.models import Job, CompanyBranch, CompanyProfile
from apps.jobs.serializers import JobSerializer

from apps.core.permissions import IsEmployer


User = get_user_model()




class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]
    lookup_field = 'id'

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'is_remote', 'employment_type', 'experience_level', 'company', 'branch', 'created_at']
    ordering_fields = ['created_at', 'updated_at', 'title', 'salary_min', 'salary_max', 'company__company_name', 'branch__name']
    ordering = ['-updated_at', '-created_at']
    search_fields = ['title']


    def perform_create(self, serializer):
        branch_id = self.request.data.get('branch_id')
        branch = None
        if branch_id:
            try:
                branch = CompanyBranch.objects.get(
                    id=branch_id,
                    company=self.request.user.company_profile
                )
            except CompanyBranch.DoesNotExist:
                raise ValidationError("Invalid branch selected")

        serializer.save(
            employer=self.request.user,
            company=self.request.user.company_profile,
            branch=branch
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

    def get_queryset(self):
        return super().get_queryset().filter(employer=self.request.user)
    

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        job.is_deleted = True
        return Response(status=204)
    





