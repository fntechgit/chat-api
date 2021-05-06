from rest_framework import serializers
from .timestamp_field import TimestampField
from ..models import AttendeeRolesService, GetStreamService
from rest_framework.exceptions import ValidationError
import logging


# Serializer without model
class UserRoleWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    inserted_at = TimestampField(read_only=True)
    updated_at = TimestampField(read_only=True)
    summit_id = serializers.IntegerField(required=True)
    member_id = serializers.IntegerField(required=True)
    idp_user_id = serializers.IntegerField(required=True)
    full_name = serializers.CharField(required=True, max_length=255)
    summit_event_id = serializers.IntegerField(initial=0, allow_null=True, required=False)

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        try:

            summit_id = validated_data['summit_id']
            idp_user_id = validated_data['idp_user_id']
            full_name = validated_data['full_name']
            member_id = validated_data['member_id']
            summit_event_id = validated_data['summit_event_id'] if 'summit_event_id' in validated_data else 0

            service = AttendeeRolesService()
            service2 = GetStreamService(summit_id)

            row = service.save({
                "summit_id": summit_id,
                "summit_event_id": summit_event_id if summit_event_id is not None else 0,
                "member_id": member_id,
                "idp_user_id": idp_user_id,
                "full_name": full_name
            })

            response = service2.create_user(
                int(row['idp_user_id']),
                str(row['full_name'])
            )

            return row
        except ValidationError as e:
            logging.getLogger('api').warning(e)
            raise
        except Exception as e:
            logging.getLogger('api').error(e)
            raise

