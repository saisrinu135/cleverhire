from django.urls import path

from apps.core.views import LocationsView, LocationRetrieveUpdateDestroyView


urlpatterns = [
    path('locations/', LocationsView.as_view(), name='locations'),
    path('locations/<uuid:id>/', LocationRetrieveUpdateDestroyView.as_view(), name='location'),
]
