from django.db import models
from django.utils import timezone


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=2, null=False, unique=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    flag = models.FileField(null=True, blank=True, upload_to="media/flags/4x3/")

    def __str__(self):
        return self.code


class LogsModel(models.Model):
    api = models.CharField(max_length=1024, help_text='API URL')
    method = models.CharField(max_length=10, db_index=True)
    client_ip_address = models.CharField(max_length=50)
    client_timezone = models.CharField(max_length=60, null=True, blank=True)
    # client_country = models.CharField(max_length=60, null=True, blank=True)
    client_country = models.ForeignKey(to=Country, on_delete=models.SET_NULL, null=True)
    status_code = models.PositiveSmallIntegerField(help_text='Response status code', db_index=True)
    execution_time = models.CharField(max_length=60, null=True, blank=True)
    added_on = models.DateTimeField(default=timezone.now)
    response = models.JSONField(null=True)

    def __str__(self):
        return self.api

    def date_created(self):
        return self.added_on.date()

    def time_created(self):
        return self.added_on.time()


#     def save(self, *args, **kwargs):
#         self._assign_country()
#         super().save(*args, **kwargs)
#
#     def country(self):
#         return self.client_country.code
#
#     def _get_country_code(self, time_zone):
#         try:
#             time_zone = f"{time_zone.split('/')[0].capitalize()}/{time_zone.split('/')[1].capitalize()}"
#             timezone_country = {}
#             for countrycode in country_timezones:
#                 timezones = country_timezones[countrycode]
#                 for timezone in timezones:
#                     timezone_country[timezone] = countrycode
#             return timezone_country[time_zone]
#         except KeyError:
#             return f'country code for {time_zone} not found'
#         except AttributeError:
#             return f'invalid param sent'
#
#     def _assign_country(self):
#         country_code = self._get_country_code(self.client_timezone)
#         self.client_country = Country.objects.filter(code=country_code)
#

