from django.contrib import admin
from django.contrib.gis import admin as gis_admin

# Register your models here.
from apps.core.models import Location


@gis_admin.register(Location)
class LocationAdmin(gis_admin.GISModelAdmin):
    list_display = ['city', 'state', 'country']
    search_fields = ['city', 'state', 'country']
    list_filter = ['country', 'state']

    # GISAdmin defaults are usually sufficient, or can be customized
    # GISAdmin defaults are usually sufficient, or can be customized
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 10,
            'default_lat': 40.7128,
            'default_lon': -74.0060,
        }
    }
