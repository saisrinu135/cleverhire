from django.urls import path

from apps.jobs.views import (
    JobListCreateAPIView,
    JobRetrieveUpdateDestroyView,
    JobPublishAPIView,
    JobCloseAPIView,
    SkillsListView,
    JobSaveAPIView
)


urlpatterns = [
    path('', view=JobListCreateAPIView.as_view(), name='job-list-create'),
    path('<uuid:id>/', view=JobRetrieveUpdateDestroyView.as_view(),
         name='job-retrieve-update-destroy'),
    path('<uuid:id>/publish/', view=JobPublishAPIView.as_view(), name='job-publish'),
    path('<uuid:id>/close/', view=JobCloseAPIView.as_view(), name='job-close'),
    path('skills/', view=SkillsListView.as_view(), name='skills'),
    path('<uuid:id>/save/', view=JobSaveAPIView.as_view(), name='job-save')
]
