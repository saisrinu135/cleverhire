from django.contrib import admin

# Register your models here.
from apps.users.models import User, Profile, CompanyProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'first_name',
                    'last_name', 'is_active', 'is_staff', 'email_token', 'is_email_verified')
    list_filter = ('role', 'is_active', 'is_staff', 'is_email_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at',
                       'role', 'is_active', 'is_staff', 'is_email_verified', 'email_token')
    actions = ['soft_delete']
    

    def soft_delete(self, request, queryset):
        for obj in queryset:
            obj.is_deleted = True
            obj.save()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'is_phone_verified', 'location', 'current_title', 'get_skills',
                    'years_of_experience', 'desired_salary_min', 'desired_salary_max', 'resume', 'is_actively_looking', 'is_open_to_remote')
    list_filter = ('is_phone_verified',
                   'is_actively_looking', 'is_open_to_remote')
    search_fields = ('full_name', 'phone', 'current_title',
                     'years_of_experience', 'desired_salary_min', 'desired_salary_max')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = 'Skills'


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_size', 'industry','get_location','location',
                    'address', 'city', 'state', 'country', 'zip_code', 'website', 'description', 'logo', 'founded_date')
    list_filter = ('company_size', 'industry', 'city', 'state', 'country')
    search_fields = ('company_name', 'company_size', 'industry')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('user',)

    def get_location(self, obj):
        return ", ".join([location.city for location in obj.locations.all()])
