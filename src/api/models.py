import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        abstract = True


class Workflow(BaseModel):
    STATUS = (
        ('inserted', 'inserted'),
        ('consumed', 'consumed'),
    )

    public_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=8, choices=STATUS)
    data = JSONField()
    steps = ArrayField(models.CharField(max_length=10, blank=True), size=8)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='created_workflows')
    produced_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.PROTECT, related_name='produced_workflows')

    def __str__(self):
        return f'{self.public_id} - {self.status}'

    class Meta:
        ordering = ['-created_at']
