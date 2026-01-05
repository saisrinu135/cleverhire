from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from apps.users.models import User
from apps.jobs.models import Job

class Application(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        REVIEWED = 'REVIEWED', _('Reviewed')
        SHORTLISTED = 'SHORTLISTED', _('Shortlisted')
        REJECTED = 'REJECTED', _('Rejected')
        ACCEPTED = 'ACCEPTED', _('Accepted')

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume_snapshot = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    match_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    ai_analysis = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('job', 'candidate')
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        db_table = 'applications'

    def __str__(self):
        return f"{self.candidate.email} applied for {self.job.title}"

class MatchScore(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='match_scores')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_scores')
    overall_score = models.FloatField(default=0.0)
    skill_match_score = models.FloatField(default=0.0)
    experience_match_score = models.FloatField(default=0.0)
    location_match_score = models.FloatField(default=0.0)
    salary_match_score = models.FloatField(default=0.0)
    calculated_at = models.DateTimeField(auto_now=True)
    score_breakdown = models.JSONField(default=dict)

    class Meta:
        unique_together = ('job', 'candidate')
        verbose_name = 'Match Score'
        verbose_name_plural = 'Match Scores'
        db_table = 'match_scores'
    
    def __str__(self):
        return f"Match: {self.candidate.email} -> {self.job.title} ({self.overall_score}%)"
