import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from .manager import UserManager, CompanyManager


class User(AbstractUser, TimeStampedModel):
    class Role(models.TextChoices):
        JOB_SEEKER = 'JOB_SEEKER', _('Job Seeker')
        EMPLOYER = 'EMPLOYER', _('Employer')
        ADMIN = 'ADMIN', _('Admin')

    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.JOB_SEEKER)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    email_token = models.CharField(
        default=None, editable=False, null=True, blank=True, unique=True)
    is_email_verified = models.BooleanField(
        default=False, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user_{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def is_job_seeker(self):
        return hasattr(self, 'profile')

    @property
    def is_employer(self):
        return self.companies.filter(is_deleted=False).exists() or self.experiences.filter(
            company__isnull=False, is_current=True).exists()


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    location = models.PointField(srid=4326, blank=True, null=True)
    current_title = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    desired_salary_min = models.IntegerField(blank=True, null=True)
    desired_salary_max = models.IntegerField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_text = models.TextField(blank=True)
    skills = models.ManyToManyField(
        'jobs.Skill', related_name='profiles', blank=True)
    is_actively_looking = models.BooleanField(default=True)
    is_open_to_remote = models.BooleanField(default=True)

    #links
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    profile_completeness = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    visibility_settings = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profiles'
    
    def calculate_completeness(self):
        """Calculate the profile completeness"""
        score = 0

        if self.full_name:
            score += 5
        if self.phone:
            score += 5
        if self.summary:
            score += 5
        if self.current_title:
            score += 10
        if self.years_of_experience:
            score += 10
        if self.resume:
            score += 10
        if self.skills.exists():
            score += 10
        
        self.profile_completeness = score
        self.save(update_fields=['profile_completeness'])

        return score
        
        



class CompanyProfile(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='companies')
    company_name = models.CharField(max_length=255)
    company_size = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    location = models.PointField(srid=4326, blank=True, null=True)
    locations = models.ManyToManyField(
        'core.Location', related_name='companies', blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    founded_date = models.DateField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    active_objects = CompanyManager()
    objects = models.Manager()

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'
        db_table = 'company_profiles'


class Experience(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='experiences')
    company = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='employee_experiences')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}'s Experience"

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
        db_table = 'experiences'


class Education(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='educations')
    institute = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True)
    field_of_study = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)