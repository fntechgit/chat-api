import logging
from ..utils import config
from supabase_py import create_client, Client
import stream
from stream.client import StreamClient


class GetStreamService:

    supabase: Client = None
    gstream: StreamClient = None

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
        self.gstream = stream.connect(row['api_key'], row['api_secret'])

    def create_user(self, user_id:int, user_full_name:str):
        response = self.gstream.users.add(str(user_id),{
            'name' : user_full_name,
            'id': str(user_id),
        }, get_or_create = True)
        return response
