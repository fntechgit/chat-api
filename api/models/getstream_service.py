import logging

from rest_framework.exceptions import ValidationError
from stream_chat.base.exceptions import StreamAPIException
from ..utils import config
from supabase_py import create_client, Client
from stream_chat import StreamChat
from django.core.cache import cache
import traceback


class GetStreamService:
    supabase: Client = None
    # https://github.com/GetStream/stream-chat-python/
    gstream: StreamChat = None
    api_key: str = None

    def __init__(self, summit_id: int):
        cache_key_api_key = 'api_key_{summit_id}'.format(summit_id=summit_id)
        cache_key_api_secret = 'api_secret_{summit_id}'.format(summit_id=summit_id)
        api_key = cache.get(cache_key_api_key)
        api_secret = cache.get(cache_key_api_secret)
        url: str = config("SUPABASE.URL")
        key: str = config("SUPABASE.KEY")

        if api_key is None or api_secret is None:
            try:
                self.supabase = create_client(url, key)
                logging.getLogger('api').debug('api_key/api_secret not found for summit {id}, trying to get it from SUPA'.format(id=summit_id))
                result = self.supabase \
                    .from_("summit_getstream_apps") \
                    .select('*') \
                    .eq("summit_id", str(summit_id)) \
                    .execute()
                if not len(result['data']):
                    raise ValidationError("Missing Summit GSTREAM Auth data.")
                row = result['data'][0]
                api_key = row['api_key']
                api_secret = row['api_secret']
                cache.set(cache_key_api_key, api_key, 7200)
                cache.set(cache_key_api_secret, api_secret, 7200)
            except ValidationError as e:
                logging.getLogger('api').warning(e)
                raise
            except Exception:
                logging.getLogger('api').error(traceback.format_exc())
                raise Exception('SUPABASE connection error')

        self.api_key = api_key
        try:
            logging.getLogger('api').debug('trying to create gstream client with key {key}'.format(key=self.api_key))
            self.gstream = StreamChat(self.api_key, api_secret=api_secret)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('GSStream connection error')

    def __del__(self):
        if self.gstream is not None:
            self.gstream = None
        if self.supabase is not None:
            self.supabase = None

    def create_user(self, user_id: int, user_full_name: str):
        try:
            response = self.gstream.update_user({
                'name': user_full_name,
                'id': str(user_id),
            })
            return response
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('create_user: GSStream connection error')

    def sso(self, user_info):
        try:
            role = "user"
            groups = user_info['user_groups']
            for group in groups:
                if group['slug'] == 'administrators' or group['slug'] == 'super-admins':
                    role = 'admin'
                    break

            user_id = user_info['user_id']
            user_first_name = user_info['user_first_name']
            user_last_name = user_info['user_last_name']
            pic = user_info['user_pic']
            user_full_name = '{} {}'.format(user_first_name, user_last_name)
            show_fullname = bool(user_info['user_public_profile_show_fullname'])

            token = self.gstream.create_token(str(user_id))

            logging.getLogger('api').debug(
                'sso user_id {} first name {} last name {} fullname {} role {}'.format(user_id, user_first_name,
                                                                                       user_last_name, user_full_name,
                                                                                       role))

            self.gstream.update_user({
                'id': str(user_id),
                'name': str(user_full_name),
                'first_name': str(user_first_name),
                'last_name': str(user_last_name),
                'role': str(role),
                'image': str(pic),
                'show_fullname': show_fullname
            })

            return {
                'id': str(user_id),
                'name': str(user_full_name),
                'first_name': str(user_first_name),
                'last_name': str(user_last_name),
                'role': str(role),
                'image': str(pic),
                'token': token,
                'api_key': self.api_key,
                'show_fullname': show_fullname
            }
        except StreamAPIException as e:
            logging.getLogger('api').warning(e)
            raise ValidationError("ERROR on GS API")
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('sso: GSStream connection error')

    def seed_channel_types(self):
        try:
            # @see https://getstream.io/chat/docs/python/resources/?language=python
            channel_types = [
                {
                    "name": "activity_room",
                    "permissions": [
                        dict(
                            name="Admin users can perform any action",
                            priority=600,
                            resources=["*"],
                            roles=["admin"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Anonymous users are not allowed",
                            priority=500,
                            resources=["*"],
                            roles=["anonymous"],
                            owner=False,
                            action="Deny",
                        ),
                        dict(
                            name="Users can modify their own messages",
                            priority=400,
                            resources=["*"],
                            roles=["user"],
                            owner=True,
                            action="Allow",
                        ),
                        dict(
                            name="Users can create channels",
                            priority=300,
                            resources=["*"],
                            roles=["user"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Channel Members",
                            priority=200,
                            resources=["ReadChannel", "CreateMessage"],
                            roles=["channel_member"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Discard all",
                            priority=100,
                            resources=["*"],
                            roles=["*"],
                            owner=False,
                            action="Deny",
                        ),
                    ],
                    "mutes": True,
                    "reactions": True,
                },
                {
                    "name": "custom_room",
                    "permissions": [
                        dict(
                            name="Admin users can perform any action",
                            priority=600,
                            resources=["*"],
                            roles=["admin"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Anonymous users are not allowed",
                            priority=500,
                            resources=["*"],
                            roles=["anonymous"],
                            owner=False,
                            action="Deny",
                        ),
                        dict(
                            name="Users can modify their own messages",
                            priority=400,
                            resources=["*"],
                            roles=["user"],
                            owner=True,
                            action="Allow",
                        ),
                        dict(
                            name="Channel Members",
                            priority=200,
                            resources=["ReadChannel", "CreateMessage"],
                            roles=["channel_member"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Discard all",
                            priority=100,
                            resources=["*"],
                            roles=["*"],
                            owner=False,
                            action="Deny",
                        ),
                    ],
                    "mutes": True,
                    "reactions": True,
                },
                {
                    "name": "qa_room",
                    "permissions": [
                        dict(
                            name="Admin users can perform any action",
                            priority=600,
                            resources=["*"],
                            roles=["admin"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Anonymous users are not allowed",
                            priority=500,
                            resources=["*"],
                            roles=["anonymous"],
                            owner=False,
                            action="Deny",
                        ),
                        dict(
                            name="Users can modify their own messages",
                            priority=400,
                            resources=["*"],
                            roles=["user"],
                            owner=True,
                            action="Allow",
                        ),
                        dict(
                            name="Channel Members",
                            priority=200,
                            resources=["ReadChannel", "CreateMessage", "CreateChannel"],
                            roles=["channel_member"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Discard all",
                            priority=100,
                            resources=["*"],
                            roles=["*"],
                            owner=False,
                            action="Deny",
                        ),

                    ],
                    "mutes": True,
                    "reactions": True,
                },
                {
                    "name": "help_room",
                    "permissions": [
                        dict(
                            name="Admin users can perform any action",
                            priority=600,
                            resources=["*"],
                            roles=["admin"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Anonymous users are not allowed",
                            priority=500,
                            resources=["*"],
                            roles=["anonymous"],
                            owner=False,
                            action="Deny",
                        ),
                        dict(
                            name="Users can modify their own messages",
                            priority=400,
                            resources=["*"],
                            roles=["user"],
                            owner=True,
                            action="Allow",
                        ),
                        dict(
                            name="Channel Members",
                            priority=200,
                            resources=["ReadChannel", "CreateMessage", "CreateChannel"],
                            roles=["channel_member"],
                            owner=False,
                            action="Allow",
                        ),
                        dict(
                            name="Discard all",
                            priority=100,
                            resources=["*"],
                            roles=["*"],
                            owner=False,
                            action="Deny",
                        ),

                    ],
                    "mutes": True,
                    "reactions": True,
                }
            ]
            responses = []
            for channel_type_def in channel_types:
                response = None
                try:
                    # try to get it first
                    logging.getLogger('api').debug('GetStreamService::seed_channel_types trying checking cache for {name}'.format(name=channel_type_def['name']))
                    response = cache.get(channel_type_def['name'])

                    if response is None:
                        logging.getLogger('api').debug('GetStreamService::seed_channel_types missing cache hit for'
                                                       '{name}'.format(name=channel_type_def['name']))
                        response = self.gstream.get_channel_type(channel_type_def['name'])
                        cache.set(channel_type_def['name'], response, 3600)
                        self.gstream.update_channel_type(channel_type_def['name'],
                                                         permissions=channel_type_def['permissions'])

                except StreamAPIException as e:
                    logging.getLogger('api').warning(e)
                    try:
                        response = self.gstream.create_channel_type(
                            channel_type_def
                        )
                    except StreamAPIException as e:
                        logging.getLogger('api').warning(e)
                if response is not None:
                    responses.append(response)

            return responses
        except StreamAPIException as e:
            logging.getLogger('api').warning(e)
            raise ValidationError("ERROR on GS API")
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('seed_channel_types: GSStream connection error')
