from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Illusion(models.Model):
    title = models.CharField(max_length=20)
    portrait_link = models.URLField(null=True, blank=True)
    landscape_link = models.URLField(null=True, blank=True)
    portrait_solution_link = models.URLField(null=True, blank=True)
    landscape_solution_link = models.URLField(null=True, blank=True)
    answer_quad_points = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    difficulty_level = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    # is_deleted = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title

    # def delete(self, *args, **kwargs):
    #     if not self.is_deleted:
    #         self.is_deleted = True
    #     return self

    def creation_date(self):
        return self.created_at.date()

    def creation_time(self):
        return self.created_at.time()


class UserResponse(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    illusion = models.ForeignKey(to=Illusion, on_delete=models.SET_NULL, null=True)
    success = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username}-{self.success}'
        # return f'{self.pk}'
