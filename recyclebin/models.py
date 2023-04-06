from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class RecycleBin(models.Model):
    db_id = models.IntegerField()
    table_id = models.CharField(max_length=100)
    data = models.JSONField()
    deleted_by = models.CharField(max_length=100)
    deleted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.table_id}-{self.db_id}"



