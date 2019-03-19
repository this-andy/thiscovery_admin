from django.db import models
import uuid

class TimeStampedModel(models.Model):
    # an abstract class that provides self-updating datetime fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
