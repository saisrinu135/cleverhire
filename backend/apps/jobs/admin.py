from django.contrib import admin

# Register your models here.
from apps.jobs.models import Skill, Job, SavedJob, SavedSearch
from apps.core.models import Location
from apps.applications.models import Application



class ApplicationInline(admin.StackedInline):
    model = Application
    extra = 0
    readonly_fields = ('created_at', 'updated_at')




@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at', 'updated_at']
    list_filter = ['category']
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['name']
    ordering = ['name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'experience_level', 'employment_type', 'is_remote']
    list_filter = ['company', 'is_remote', 'is_deleted', 'status', 'employment_type', 'experience_level']
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['title', 'company__company_name']
    inlines = (ApplicationInline,)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'created_at']
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_params', 'alert_frequency','is_active','created_at']
    list_filter = ['user', 'alert_frequency']
    readonly_fields = ('created_at', 'updated_at')
    actions = ['make_inactive']

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

