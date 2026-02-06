from django.contrib import admin

# Register your models here.
from apps.users.models import User, Profile, CompanyProfile, Experience, Education



class WorkExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0


class EducationInline(admin.StackedInline):
    model = Education
    extra = 0

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_active', 'is_staff', 'is_email_verified', 'profile_link')
    list_filter = ('role', 'is_active', 'is_staff', 'is_email_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at',
                       'role', 'is_staff', 'is_email_verified', 'email_token', 'password')
    actions = ['soft_delete']
    inlines = (ProfileInline, WorkExperienceInline, EducationInline)

    def get_queryset(self, request):
        return User.objects.all()
    
    def profile_link(self, obj):
        if hasattr(obj, 'profile'):
            from django.urls import reverse
            from django.utils.html import format_html
            url = reverse('admin:users_profile_change', args=[obj.profile.id])
            return format_html('<a href="{}">View Profile</a>', url)
        return '-'
    profile_link.short_description = 'Profile'

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

    fieldsets = (
        ("User", {
            "fields": ('user',)
        }),
        ('Basic Information', {
            'fields': ('full_name', 'phone', 'location')
        }),
        ('Experience', {
            "fields": ('headline','current_title', 'years_of_experience', 'summary')
        }),
        ('Salary Expectiations', {
            'fields': ('desired_salary_min', 'desired_salary_max')
        }),
        ('Resume', {
            'fields': ('resume', 'resume_text')
        }),
        ("Skills", {
            'fields': ('skills',)
        }),
        ('Status', {
            'fields': ('is_actively_looking', 'is_open_to_remote')
        })
    )

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = 'Skills'


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company_name', 'company_size', 'industry','operating_locations','location',
                    'address', 'city', 'state', 'country', 'zip_code', 'website', 'description', 'logo', 'founded_date', 'is_deleted')
    list_filter = ('industry', 'city', 'state', 'country', 'is_deleted')
    search_fields = ('company_name', 'industry')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('user',)
    actions = ['restore_companies', 'restore_all_companies', 'soft_delete']


    def operating_locations(self, obj):
        return ", ".join([location.city for location in obj.locations.all()])

    def get_queryset(self, request):
        return CompanyProfile.objects.all()


    def restore_companies(self, request, queryset):
        for obj in queryset:
            obj.is_deleted = False
            obj.save()
    
    def restore_all_companies(self, request, queryset):
        CompanyProfile.objects.all().update(is_deleted=False)
    
    def soft_delete(self, request, queryset):
        for obj in queryset:
            obj.is_deleted = True
            obj.save()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'company_name', 'title', 'start_date', 'end_date', 'description', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('company_name', 'title')
    ordering = ('-created_at',)
    readonly_fields = ('user','created_at', 'updated_at')
    list_select_related = ('user', 'company')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'institute', 'degree', 'field_of_study')
    readonly_fields = ('created_at', 'updated_at')