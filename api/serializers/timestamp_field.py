from rest_framework import serializers
import datetime


class TimestampField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, date_str: str):
        #str_to_dt = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        str_to_dt = datetime.datetime.fromisoformat(date_str)
        return int(str_to_dt.timestamp())