from ..serializers.timestamp_field import TimestampField
from django.test import TestCase


class TestTimeStampField(TestCase):

    def test_format(self):
        f = TimestampField()
        f.to_representation(date_str="2021-08-16T03:51:06+00:00")
