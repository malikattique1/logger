from django.contrib import admin
from django.forms import model_to_dict
from .models import Illusion, UserResponse
from recyclebin.models import RecycleBin
from django.utils import timezone


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        illusion_dict = model_to_dict(obj)
        illusion_dict['created_at'] = obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        illusion_dict['updated_at'] = obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        recycle_bin = RecycleBin.objects.create(
            db_id=obj.id,
            table_id=obj._meta.model_name,
            data=illusion_dict,
            deleted_by=request.user.username,
            deleted_at=timezone.now()
        )
        print(recycle_bin)
    queryset.delete()


@admin.register(Illusion)
class IllusionAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    list_display = [

        'id',
        # 'is_deleted',
        'title',
        'portrait_link',
        'landscape_link',
        'portrait_solution_link',
        'landscape_solution_link',
        'answer_quad_points',
        'points',
        'difficulty_level',
        'status',
        'creation_date',
        'created_at',
        'updated_at',
    ]
    list_filter = ['title', 'created_at']
    list_editable = ['status', 'points']
    # list_editable = ['is_deleted', 'status', 'points']

    # def restore_selected_objects(self, obj):
    #     def restore(self):
    #         if self.is_deleted:
    #             self.is_deleted = False
    #         else:
    #             pass


admin.site.register(UserResponse)
