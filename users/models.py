from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=200, unique=True)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    # def __str__(self):
    #     return f'profile: {self.user.username}'

    def username(self):
        return self.user.username

    # def delete(self, *args, **kwargs):
    #     if obj is not None:
    #         return self.delete()
    #     else:
    #         pass
