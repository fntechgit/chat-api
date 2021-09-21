import logging
import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..security import OAuth2Authentication, oauth2_scope_required
from ..serializers import UserRoleWriteSerializer
from ..models import AttendeeRolesService
from rest_framework.settings import api_settings
import os
from ..models import GetStreamService


class UserRolesListAPIView(ViewSet):
    serializer_class = UserRoleWriteSerializer

    def list(self, request, *args, **kwargs):
        service = AttendeeRolesService()
        summit_id = int(request.query_params.get('summit_id', 0))
        if not summit_id:
            raise ValidationError("summit_id is mandatory.")

        summit_event_id = int(request.query_params.get('summit_event_id', 0))
        if summit_event_id > 0:
            page = service.list_qa_users(
                summit_id,
                summit_event_id
            )
        else:
            page = service.list_help_users(
                summit_id
            )
        serializer = UserRoleWriteSerializer(instance=page, many=True)
        return Response(serializer.data)


class UserRolesCreateAPIView(ViewSet):
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
    def remove(self, request, *args, **kwargs):
        try:
            logging.getLogger('api').debug('calling UserRolesListCreateAPIView::remove')
            summit_id = int(request.query_params.get('summit_id', 0))
            summit_event_id = int(request.query_params.get('summit_event_id', 0))
            member_id = int(request.query_params.get('member_id', 0))
            if not summit_id:
                raise ValidationError("summit_id is mandatory.")
            if not member_id:
                raise ValidationError("member_id is mandatory.")
            service = AttendeeRolesService()
            if summit_event_id > 0:
                service.remove_qa(summit_id, member_id, summit_event_id)
            else:
                service.remove_help(summit_id, member_id)
            return Response("", status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            logging.getLogger('api').warning(e)
            return Response(e.detail, status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            return Response('server error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @oauth2_scope_required()
    def create(self, request, *args, **kwargs):
        try:
            logging.getLogger('api').debug('calling UserRolesListCreateAPIView::create')
            serializer = UserRoleWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logging.getLogger('api').warning(e)
            return Response(e.detail, status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            return Response('server error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @oauth2_scope_required()
    def sso(self, request, token_info , *args, **kwargs):
        try:
            logging.getLogger('api').debug('calling UserRolesListCreateAPIView::sso')
            summit_id = int(request.query_params.get('summit_id', 0))

            if not summit_id:
                raise ValidationError("summit_id is mandatory.")

            service = GetStreamService(summit_id)
            res = service.sso(token_info)

            return Response(res, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logging.getLogger('api').warning(e)
            return Response(e.detail, status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            return Response('server error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
