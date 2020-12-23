from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.user_service.models import User


class FoundNoticeTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(username='john', password=make_password('secret'), first_name='Thu',
                                        last_name='Student',
                                        is_verified=True, status='ACT', is_staff=False, is_superuser=False,
                                        date_joined=make_aware(datetime.now()))
        self.property_type = PropertyType.objects.create(name='electronic')
        self.property_template = PropertyTemplate.objects.create(name='iphone', type=self.property_type,
                                                                 fields='{"serial": 123}')

        self.notice = FoundNotice.objects.create(
            property=Property.objects.create(name='My Iphone', template=self.property_template,
                                             attributes='{"serial": 123}'),
            found_location='{"name": "清华大学紫荆学生公寓4号楼","address": "北京市海淀区 ", \
                          "latitude": 40.0104, "longitude": 116.327391}"',
            found_datetime='2020-02-20 11:11',
            author=self.user
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create(self):
        data = {
            "contacts": [
                {
                    "name": "bob",
                    "method": "PHN",
                    "details": "1234"
                }
            ],
            "property": {
                "template": "iphone",
                "tags": [
                ],
                "name": "My New Iphone",
                "attributes": {"serial": 123},
                "description": "My Lost Iphone"
            },
            "description": "My Found Notice",
            "found_datetime": "2020-02-20 11:11",
            "found_location": '{"name": "清华大学紫荆学生公寓4号楼","address": "北京市海淀区 ", \
                          "latitude": 40.0104, "longitude": 116.327391}"',
            "status": "PUB"
        }
        response = self.client.post('/api/v1/found-notices/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        get_response = self.client.get('/api/v1/found-notices/2/?format=json')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()['id'], 2)

    def test_list(self):
        response = self.client.get('/api/v1/found-notices/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_detail(self):
        response = self.client.get(f'/api/v1/found-notices/{self.notice.id}/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.notice.id)

    def test_update(self):
        data = {
            "contacts": [
                {
                    "name": "bob",
                    "method": "PHN",
                    "details": "1234"
                }
            ],
            "property": {
                "template": "iphone",
                "tags": [
                ],
                "name": "My New Iphone",
                "attributes": {"serial": 123},
                "description": "My Lost Iphone"
            },
            "description": "My New Description",
            "found_datetime": "2020-02-20 11:11",
            "found_location": '{"name": "清华大学紫荆学生公寓4号楼","address": "北京市海淀区 ", \
                          "latitude": 40.0104, "longitude": 116.327391}"',
            "status": "PUB"
        }
        response = self.client.patch(f'/api/v1/found-notices/{self.notice.id}/?format=json',
                                     data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['description'], 'My New Description')

    def test_change_status(self):
        response = self.client.post(f'/api/v1/found-notices/{self.notice.id}/change-status/?format=json',
                                    {'status': 'CLS'})
        self.assertEqual(response.status_code, 200)
        get_response = self.client.get(f'/api/v1/found-notices/{self.notice.id}/?format=json')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()['status'], 'CLS')

    def test_delete(self):
        response = self.client.delete(f'/api/v1/found-notices/{self.notice.id}/?format=json')
        self.assertEqual(response.status_code, 204)
        get_response = self.client.get('/api/v1/found-notices/?format=json')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json()['results']), 0)
