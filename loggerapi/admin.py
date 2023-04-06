from django.contrib import admin
from .models import LogsModel, Country


# from django.utils.html import format_html
# from django.utils.safestring import mark_safe


# Register your models here.

@admin.register(LogsModel)
class LogsModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'api',
        'method',
        'client_ip_address',
        'client_timezone',
        'client_country',
        'status_code',
        'execution_time',
        'date_created',
        'time_created',
        'response',
    ]
    list_filter = ['method']
    list_editable = ['api']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'code',
        'latitude',
        'longitude',
        'flag',
        # 'flag_tag',
    ]

    # def flag_tag(self, obj):
    #     return format_html('<object type="image/svg+xml" data="{}" width="30" height="30">{}</object>', obj.flag.url, "SVG not supported by your browser")
    # flag_tag.short_description = 'Flag'
