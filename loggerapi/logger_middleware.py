import threading
# from loggerapi.functions import logger_request
import time
import json

from .models import Country
from .serializers import LoggerSerializer
from pytz import country_timezones


class LoggerMiddleware:
    def __init__(self, get_response):
        # print("ress", get_response)
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ['/api/']
        response = None  # define a default value for response
        for path in allowed_paths:
            if request.path.startswith(path):
                start_time = time.monotonic()
                response = self.get_response(request)
                # print('response', response)
                # print(response.content.decode())
                end_time = time.monotonic()
                execution_time = end_time - start_time
                status_code = response.status_code
                thread = threading.Thread(target=logger_request, args=(request, status_code, execution_time, response))
                thread.start()
                break  # exit the loop after handling the request
        if response is None:
            response = self.get_response(request)
        # print('response', response)
        return response


def logger_request(request, status_code, execution_time, response):

    print("respo", response)
    print("execution_time", execution_time)
    full_url = request.build_absolute_uri()
    print("full_url", full_url)
    client_ip_address = request.META.get('REMOTE_ADDR')
    # client_ip_address = '119.12.33.32'
    # with urllib.request.urlopen(f'https://ipinfo.io/{client_ip_address}/json') as url:
    #     data = json.loads(url.read().decode())
    timezone = request.GET.get('timezone', "not sent")
    print("timezone", timezone)
    country_code = get_country_code(timezone)
    print("country_code", country_code)

    if country_code:
        country, created = Country.objects.get_or_create(code=country_code)
        if created:
            pass
        client_country_id = country.pk
        print("country_code", client_country_id)

    resdata = response.content.decode()
    # print('resdata', resdata)
    json_response = json.loads(resdata)

    validated_data = {
        'api': full_url,
        'method': request.method,
        'client_ip_address': client_ip_address,
        'client_timezone': timezone,
        'client_country': client_country_id,
        'status_code': status_code,
        'execution_time': execution_time,
        'response': json_response,
    }
    serializer = LoggerSerializer(data=validated_data)
    if serializer.is_valid():
        serializer.save()
        return True
    print("f", serializer.errors)
    return False


def get_country_code(time_zone):
    try:
        print(time_zone)
        if (time_zone == "not sent"):
            return f'timezone not sent'
        else:
            time_zone = f"{time_zone.split('/')[0].capitalize()}/{time_zone.split('/')[1].capitalize()}"
            timezone_country = {}
            for countrycode in country_timezones:
                timezones = country_timezones[countrycode]
                for timezone in timezones:
                    timezone_country[timezone] = countrycode
            return timezone_country[time_zone]
    except KeyError:
        return f'country code for {time_zone} not found'
    except AttributeError:
        return f'invalid param sent'
