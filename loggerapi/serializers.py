from rest_framework import serializers
from .models import LogsModel


class LoggerSerializer(serializers.ModelSerializer):
    # api = serializers.CharField(required=False)
    # method = serializers.CharField(required=False)
    # client_ip_address = serializers.CharField(required=False)
    # client_timezone = serializers.CharField(required=False, allow_blank=True)
    # client_country = serializers.CharField(required=False, allow_blank=True)
    # status_code = serializers.IntegerField(required=False, min_value=0)
    # execution_time = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = LogsModel
        fields = [
            'id',
            'api',
            'method',
            'client_ip_address',
            'client_timezone',
            'client_country',
            'status_code',
            'execution_time',
            'added_on',
            'response'
        ]

    def create(self, validated_data):
        return LogsModel.objects.create(**validated_data)




