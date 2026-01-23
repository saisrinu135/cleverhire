from django.urls import path

from apps.jobs.views import (
    JobListCreateAPIView,
    JobRetrieveUpdateDestroyView,
    JobPublishAPIView,
    JobCloseAPIView,
    SkillsListView
)


urlpatterns = [
    path('', view=JobListCreateAPIView.as_view(), name='job-list-create'),
    path('<int:id>/', view=JobRetrieveUpdateDestroyView.as_view(),
         name='job-retrieve-update-destroy'),
    path('<int:id>/publish/', view=JobPublishAPIView.as_view(), name='job-publish'),
    path('<int:id>/close/', view=JobCloseAPIView.as_view(), name='job-close'),
    path('skills/', view=SkillsListView.as_view(), name='skills'),
]
