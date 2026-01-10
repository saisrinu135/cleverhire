from django.contrib.gis.db import models
import uuid


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created_at' and 'updated_at' fields and UUID primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(TimeStampedModel):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    coordinates = models.PointField(srid=4326, blank=True, null=True)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        db_table = 'locations'

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"
