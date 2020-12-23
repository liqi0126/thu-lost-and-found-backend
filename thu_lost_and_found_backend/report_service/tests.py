from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.user_service.models import User


# Create your tests here.
class ReportTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(username='john', password=make_password('secret'), first_name='Thu',
                                        last_name='Student',
                                        is_verified=True, status='ACT', is_staff=False, is_superuser=False,
                                        date_joined=make_aware(datetime.now()))
        self.property_type = PropertyType.objects.create(name='electronic')
        self.property_template = PropertyTemplate.objects.create(name='iphone', type=self.property_type,
                                                                 fields='{"serial": 123}')

        self.notice = LostNotice.objects.create(
            property=Property.objects.create(name='My Iphone', template=self.property_template,
                                             attributes='{"serial": 123}'),
            lost_location='{"name": "清华大学紫荆学生公寓4号楼","address": "北京市海淀区 ", \
                          "latitude": 40.0104, "longitude": 116.327391}"',
            author=self.user
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create(self):
        data = {
            "type": "HRS",
            "notice_type": "LST",
            "lost_notice": 1,
            "user": 1
        }
        response = self.client.post('/api/v1/reports/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        get_response = self.client.get('/api/v1/reports/?format=json')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json()['results']), 1)
