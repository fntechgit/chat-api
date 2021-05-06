from django.test import TestCase
from ..models import AttendeeRolesService
from ..models import GetStreamService


class TestAttendeeRoleService(TestCase):

    def test_add(self):
        summit_id = 1
        service = AttendeeRolesService()
        service2 = GetStreamService(summit_id)
        row = service.save({
            "summit_id" : summit_id,
            "summit_event_id": 1,
            "member_id": 1,
            "idp_user_id":1,
            "full_name": "Sebastian Marcet"
        })
        response = service2.create_user(row['idp_user_id'], row['full_name'])
        self.assertNotEqual(response, None)


    def test_remove_qa(self):
        service = AttendeeRolesService()
        service.save({
            "summit_id": 2,
            "summit_event_id": 2,
            "member_id": 2,
            "idp_user_id": 2,
            "full_name": "Sebastian Marcet2"
        })
        service.remove_qa(2,2,2)

    def test_remove_help(self):
        service = AttendeeRolesService()
        service.save({
            "summit_id": 2,
            "member_id": 2,
            "idp_user_id": 2,
            "full_name": "Sebastian Marcet2"
        })
        service.remove_help(2,2)

    def test_get_all_qa_users(self):
        service = AttendeeRolesService()
        service.save({
            "summit_id": 1,
            "summit_event_id": 1,
            "member_id": 1,
            "idp_user_id": 1,
            "full_name": "Sebastian Marcet"
        })
        service.save({
            "summit_id": 1,
            "summit_event_id": 1,
            "member_id": 2,
            "idp_user_id": 2,
            "full_name": "Sebastian Marcet2"
        })

        page = service.list_qa_users(1,1)

        self.assertEqual(len(page), 2)

    def test_get_all_help_users(self):
        service = AttendeeRolesService()
        service.save({
            "summit_id": 1,
            "member_id": 1,
            "idp_user_id": 1,
            "full_name": "Sebastian Marcet"
        })
        service.save({
            "summit_id": 1,
            "member_id": 2,
            "idp_user_id": 2,
            "full_name": "Sebastian Marcet2"
        })
        service.save({
            "summit_id": 2,
            "member_id": 2,
            "idp_user_id": 2,
            "full_name": "Sebastian Marcet2"
        })

        page = service.list_help_users(1)

        self.assertEqual(len(page), 2)

