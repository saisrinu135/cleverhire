from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, Location
from apps.users.models import User, CompanyProfile
from apps.jobs.manager import JobModelManager


class Skill(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    elasticsearch_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        db_table = 'skills'


class Job(TimeStampedModel):
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', _('Entry Level')
        MID = 'MID', _('Mid Level')
        SENIOR = 'SENIOR', _('Senior Level')
        EXECUTIVE = 'EXECUTIVE', _('Executive')

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', _('Full Time')
        PART_TIME = 'PART_TIME', _('Part Time')
        CONTRACT = 'CONTRACT', _('Contract')
        INTERNSHIP = 'INTERNSHIP', _('Internship')

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        CLOSED = 'CLOSED', _('Closed')

    employer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posted_jobs'
    )
    company = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name='jobs', default=None, blank=True, null=True
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name='jobs', null=True, blank=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    is_remote = models.BooleanField(default=False)
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    experience_level = models.CharField(
        max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    employment_type = models.CharField(
        max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    required_skills = models.ManyToManyField(Skill, related_name='jobs')
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT)
    expires_at = models.DateTimeField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    application_count = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    active_objects = JobModelManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        db_table = 'jobs'


class SavedJob(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='saved_by')

    class Meta:
        unique_together = ('user', 'job')
        verbose_name = 'Saved Job'
        verbose_name_plural = 'Saved Jobs'
        db_table = 'saved_jobs'

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"


class SavedSearch(TimeStampedModel):
    class Frequency(models.TextChoices):
        DAILY = 'DAILY', _('Daily')
        WEEKLY = 'WEEKLY', _('Weekly')
        INSTANT = 'INSTANT', _('Instant')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='saved_searches')
    query_params = models.JSONField(default=dict)
    alert_frequency = models.CharField(
        max_length=20, choices=Frequency.choices, default=Frequency.DAILY)
    is_active = models.BooleanField(default=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Search by {self.user.email}"

    class Meta:
        verbose_name = 'Saved Search'
        verbose_name_plural = 'Saved Searches'
        db_table = 'saved_searches'
