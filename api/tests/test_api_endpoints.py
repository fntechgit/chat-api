from rest_framework.test import APITestCase
from django.urls import reverse
import json
from rest_framework import status


class ApiEndpointTest(APITestCase):

    def test_add_user_role(self):
        access_token = 'TGzJUbuWKOtKrrn81.TDWcZrYLiaBH3WQT1b25OtLf26TTKyFNnnONcL-jPUQOHcD_0eT8p2Pcopr1PaCd6kPfaL1Y10FgeChreKfm2b8du8HRgWpk6N8auXX0z33RJN&'
        url = reverse('user-roles-write:create')

        data = {
            "full_name": "Allen Altostratus",
            "idp_user_id": 10,
            "member_id": 245,
            "summit_event_id": 0,
            "summit_id": 17
        }

        response = self.client.post('{url}?access_token={access_token}'.format(url=url, access_token=access_token),
                                    data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_seed_channel_types(self):
        access_token = 'ACCESS_TOKEN'
        url = reverse('channel_types:seed')

        data = {}

        response = self.client.post(
            '{url}?access_token={access_token}&summit_id=17'.format(url=url, access_token=access_token),
            data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sso(self):
        access_token = 'ACCESS_TOKEN'
        url = reverse('user-sso:sso')

        data = {}

        response = self.client.post(
            '{url}?access_token={access_token}&summit_id=17'.format(url=url, access_token=access_token),
            data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sso_auth_data_not_found(self):
        access_token = 'ACCESS_TOKEN'
        url = reverse('user-sso:sso')

        data = {}

        response = self.client.post(
            '{url}?access_token={access_token}&summit_id=1'.format(url=url, access_token=access_token),
            data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
