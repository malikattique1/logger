from django.contrib import admin
from django.forms import model_to_dict
from recyclebin.models import RecycleBin
from .models import UserProfile
from django.utils.safestring import mark_safe
from django.utils import timezone


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        user_dict = model_to_dict(obj)
        if hasattr(UserProfile, 'image'):
            user_dict['image'] = str(UserProfile.image)

        recycle_bin = RecycleBin.objects.create(
            db_id=obj.id,
            table_id=obj._meta.model_name,
            data=user_dict,
            deleted_by=request.user.username,
            deleted_at=timezone.now()
        )
        print(recycle_bin)
    queryset.delete()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    actions = [delete_selected]

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="30" height="30" />'.format(obj.image.url))

    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag']

    list_display = ['image_tag', 'id', 'username', 'unique_id', 'image']
    fields = [('image_tag', 'username'), 'id']


