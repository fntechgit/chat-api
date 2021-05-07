import logging
import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..security import OAuth2Authentication, oauth2_scope_required
from ..serializers import UserRoleWriteSerializer
from rest_framework.settings import api_settings
from ..models import GetStreamService
import os


class ChannelTypesAPIView(ViewSet):
    authentication_classes = [] if os.getenv("ENV") == 'test' else [OAuth2Authentication]

    serializer_class = UserRoleWriteSerializer

    @staticmethod
    def perform_create(serializer):
        serializer.save()

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @oauth2_scope_required()
    def seed(self, request, *args, **kwargs):
        try:
            logging.getLogger('api').debug('calling ChannelTypesAPIView::seed')
            summit_id = int(request.query_params.get('summit_id', 0))
            if not summit_id:
                raise ValidationError("summit_id is mandatory.")
            service = GetStreamService(summit_id)
            responses = service.seed_channel_types()
            return Response(responses, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logging.getLogger('api').warning(e)
            return Response(e.detail, status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            return Response('server error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)