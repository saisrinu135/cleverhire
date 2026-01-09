from django.contrib import admin

# Register your models here.
from apps.jobs.models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at', 'updated_at']
    list_filter = ['category']
    readonly_fields = ('created_at', 'updated_at')