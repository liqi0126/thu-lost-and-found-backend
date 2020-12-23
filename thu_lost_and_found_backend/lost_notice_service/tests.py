from datetime import datetime

from django.test import TestCase, Client
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate
from thu_lost_and_found_backend.user_service.models import User


class LostNoticeTestCase(TestCase):
    def setUp(self):

        client = Client()
        
        user = User.objects.create(username='john', password='secret', first_name='Thu', last_name='Student',
                                   is_verified=True, status='ACT', is_staff=False, is_superuser=False,
                                   date_joined=datetime.now())
        property_type = PropertyType.objects.create(name='electronic')
        property_template = PropertyTemplate.objects.create(name='iphone', type=property_type)

    def test_create(self):
        pass

    def test_read(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass
