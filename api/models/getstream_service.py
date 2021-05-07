import logging

from stream_chat.base.exceptions import StreamAPIException

from ..utils import config
from supabase_py import create_client, Client
from stream_chat import StreamChat


class GetStreamService:

    supabase: Client = None
    # https://github.com/GetStream/stream-chat-python/
    gstream: StreamChat = None

    def __init__(self, summit_id:int):
        url: str = config("SUPABASE.URL")
        key: str = config("SUPABASE.KEY")
        self.supabase = create_client(url, key)
        result = self.supabase\
            .from_("summit_getstream_apps")\
            .select('*') \
            .eq("summit_id", str(summit_id)) \
            .execute()
        if not len(result['data']):
            raise Exception("Missing Summit GSTREAM Auth data.")

        row = result['data'][0]
        self.gstream = StreamChat(api_key=row['api_key'], api_secret=row['api_secret'])

    def create_user(self, user_id:int, user_full_name:str):
        response = self.gstream.update_user({
            'name' : user_full_name,
            'id': str(user_id),
        })
        return response

    def seed_channel_types(self):

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
                        resources= ["ReadChannel", "CreateMessage"],
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
            }
        ]
        responses = []
        for channel_type_def in channel_types:
            response = None
            try:
                # try to get it first
                response = self.gstream.get_channel_type(channel_type_def['name'])
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