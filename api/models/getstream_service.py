import logging

from stream_chat.base.exceptions import StreamAPIException

from ..utils import config
from supabase_py import create_client, Client
from stream_chat import StreamChat
from django.core.cache import cache


class GetStreamService:
    supabase: Client = None
    # https://github.com/GetStream/stream-chat-python/
    gstream: StreamChat = None
    api_key: str = None

    def __init__(self, summit_id: int):
        url: str = config("SUPABASE.URL")
        key: str = config("SUPABASE.KEY")
        self.supabase = create_client(url, key)
        result = self.supabase \
            .from_("summit_getstream_apps") \
            .select('*') \
            .eq("summit_id", str(summit_id)) \
            .execute()
        if not len(result['data']):
            raise Exception("Missing Summit GSTREAM Auth data.")

        row = result['data'][0]
        self.api_key = row['api_key']
        self.gstream = StreamChat(self.api_key, api_secret=row['api_secret'])

    def create_user(self, user_id: int, user_full_name: str):
        response = self.gstream.update_user({
            'name': user_full_name,
            'id': str(user_id),
        })
        return response

    def sso(self, user_info):

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

    def seed_channel_types(self):
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
