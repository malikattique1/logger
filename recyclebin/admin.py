from django.contrib import admin
from .models import RecycleBin
from core.models import Illusion
from rest_framework.utils import json
from users.models import UserProfile
from django.contrib.auth.models import User


def restore_selected_objects(modeladmin, request, queryset):
    for recyclebin_obj in queryset:
        illusion_data = json.loads(json.dumps(recyclebin_obj.data))
        illusion_obj = Illusion(**illusion_data)
        illusion_obj.save()
        recyclebin_obj.delete()


restore_selected_objects.short_description = "Restore selected illusion"


# def restore_selected_users(modeladmin, request, queryset):
#     for recyclebin_obj in queryset:
#         user_data = json.loads(json.dumps(recyclebin_obj.data))
#         user_obj = UserProfile(**user_data)
#         user_obj.save()
#         recyclebin_obj.delete()
#
#
# restore_selected_objects.short_description = "Restore selected users"


# def restore_selected_users(modeladmin, request, queryset):
#     for recyclebin_obj in queryset:
#         user_data = json.loads(json.dumps(recyclebin_obj.data))
#         if 'username' in user_data:
#             user_obj, created = User.objects.get_or_create(username=user_data['username'])
#
#             if created:
#                 user_obj.set_password(user_data['password'])
#                 user_obj.save()
#                 user_profile_data = user_data.get('user_profile')
#                 user_profile_data['user'] = user_obj
#                 user_profile_obj = UserProfile(**user_profile_data)
#                 user_profile_obj.save()
#
#         recyclebin_obj.delete()


class RecycleBinAdmin(admin.ModelAdmin):
    actions = [restore_selected_objects]
    # actions = [restore_selected_users]

    list_display = [
        'id',
        'db_id',
        'table_id',
        'data',
        'deleted_by',
        'deleted_at'
    ]
    list_filter = ['id']
    list_editable = ['data']


admin.site.register(RecycleBin, RecycleBinAdmin)
