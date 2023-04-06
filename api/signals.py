from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import Image
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_User_token(sender, instance, created, **kwargs):
    print('token signal called')
    if created:
        Token.objects.create(user=instance)
