import logging
from ..utils import config
from supabase_py import create_client, Client
from json.decoder import JSONDecodeError
from rest_framework.exceptions import ValidationError
import traceback


class AttendeeRolesService:

    supabase: Client = None

    def __init__(self):
        try:
            url: str = config("SUPABASE.URL")
            key: str = config("SUPABASE.KEY")
            self.supabase = create_client(url, key)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('SUPABASE connection error')

    def __del__(self):
        if self.supabase is not None:
            self.supabase = None

    def save(self, payload):
        try:
            summit_id = payload['summit_id']
            member_id = payload['member_id']
            summit_event_id = payload['summit_event_id'] if "summit_event_id" in payload else 0
            idp_user_id = payload['idp_user_id']
            full_name = payload['full_name']
            result = self.supabase.table("summit_attendee_roles").insert(
                {"summit_id": summit_id,
                 "member_id": member_id,
                 "summit_event_id": summit_event_id,
                 "idp_user_id" : idp_user_id,
                 "full_name" : full_name
                 }).execute()
            if result['status_code'] != 201:
                raise ValidationError(result['data']['message'])
            return result['data'][0]
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('SUPABASE connection error')

    def remove_qa(self, summit_id:int , member_id:int, summit_event_id: int ):
        try:
            self.supabase\
                .from_("summit_attendee_roles") \
                .delete() \
                .eq("summit_id", str(summit_id)) \
                .eq("member_id", str(member_id)) \
                .eq("summit_event_id", str(summit_event_id))\
                .execute()
        except JSONDecodeError as e:
            logging.getLogger('api').error(e)
        except Exception as e:
            logging.getLogger('api').error(e)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('SUPABASE connection error')

    def remove_help(self, summit_id: int, member_id: int):
        try:
            self.supabase.from_("summit_attendee_roles") \
                .delete() \
                .eq("summit_id", str(summit_id)) \
                .eq("member_id", str(member_id)) \
                .eq("summit_event_id", "0")\
                .execute()
        except JSONDecodeError as e:
            logging.getLogger('api').error(e)
        except Exception as e:
            logging.getLogger('api').error(e)
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('SUPABASE connection error')

    def list_qa_users(self, summit_id:int, summit_event_id:int, page:int = 1, page_size:int = 10):
        try:
            _from = (page - 1) * page_size
            _to = _from + page_size
            result = self.supabase.table("summit_attendee_roles")\
                .select('*') \
                .eq("summit_id", str(summit_id)) \
                .eq("summit_event_id", str(summit_event_id)) \
                .range(_from, _to) \
                .execute()
            return result['data']
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('SUPABASE connection error')

    def list_help_users(self, summit_id: int, page:int = 1, page_size:int = 10):
        try:
            _from = (page - 1) * page_size
            _to = _from + page_size
            result = self.supabase.table("summit_attendee_roles")\
                .select('*') \
                .eq("summit_id", str(summit_id)) \
                .eq("summit_event_id", "0") \
                .range(_from, _to)\
                .execute()
            return result['data']
        except:
            logging.getLogger('api').error(traceback.format_exc())
            raise Exception('SUPABASE connection error')

