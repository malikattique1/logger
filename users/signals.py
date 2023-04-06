# from django.contrib.auth.models import User
# from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver, Signal
from .models import UserProfile

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


create_user_profile = Signal()


@receiver(create_user_profile)
def create_uniqueid_and_image(sender, **kwargs):
    print('received_custom signal')
    print(kwargs)
    # user_id = kwargs.get('instance')
    # unique_id = kwargs.get('unique_user_id')
    if kwargs.get('image'):
        UserProfile.objects.create(user_id=kwargs.get('instance'), unique_id=kwargs.get('unique_user_id'),
                                   image=kwargs.get('image'))
    else:
        UserProfile.objects.create(user_id=kwargs.get('instance'), unique_id=kwargs.get('unique_user_id'))
