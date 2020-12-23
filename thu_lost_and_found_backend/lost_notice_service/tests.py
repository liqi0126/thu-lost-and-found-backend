from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.utils.timezone import make_aware

from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.user_service.models import User


class LostNoticeTestCase(TestCase):
    client = Client()

    def setUp(self):
        user = User.objects.create(username='john', password=make_password('secret'), first_name='Thu',
                                   last_name='Student',
                                   is_verified=True, status='ACT', is_staff=False, is_superuser=False,
                                   date_joined=make_aware(datetime.now()))
        property_type = PropertyType.objects.create(name='electronic')
        property_template = PropertyTemplate.objects.create(name='iphone', type=property_type,
                                                            fields='{"serial": 123}')

        lostnotice = LostNotice.objects.create(
            property=Property.objects.create(name='My Iphone', template=property_template,
                                             attributes='{"serial": 123}'),
            lost_location='{"name": "清华大学紫荆学生公寓4号楼","address": "北京市海淀区 ", \
                          "latitude": 40.0104, "longitude": 116.327391}"',
            author=user
        )
        lostnotice.save()

    def test_create(self):
        self.client.login(username='john', password='secret')
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
            "description": "My Lost Notice",
            "lost_location": '{"name": "清华大学紫荆学生公寓4号楼","address": "北京市海淀区 ", \
                          "latitude": 40.0104, "longitude": 116.327391}"',
            "status": "PUB"
        }
        response = self.client.post('/api/v1/lost-notices/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        get_response = self.client.get('/api/v1/lost-notices/2/?format=json')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()['id'], 2)

    def test_list(self):
        response = self.client.get('/api/v1/lost-notices/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_detail(self):
        response = self.client.get('/api/v1/lost-notices/1/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

    def test_update(self):
        pass

    def test_delete(self):
        pass
