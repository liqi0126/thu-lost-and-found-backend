from django.utils.dateparse import parse_datetime
from rest_framework.test import APITestCase
from rest_framework import status

from .models import MatchingHyperParam, MatchingEntry
from .match import matching

from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.user_service.models import User


from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class MatchingHyperTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='js@js.com', password='js.sj', is_superuser=True)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_hyper(self):
        response = self.client.get('/api/v1/matching-hyperparameters/get-hyper/')
        self.assertIn('matching_threshold', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_hyper(self):
        data = {
            'matching_threshold': 0.1
        }
        response = self.client.post('/api/v1/matching-hyperparameters/update-hyper/', data, form='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/v1/matching-hyperparameters/get-hyper/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['matching_threshold'], 0.1)


class MatchingEntryTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="123@qq.com")
        self.user1.save()
        self.user2 = User.objects.create(email="456@qq.com")
        self.user2.save()

        self.card = PropertyType(name="卡片")
        self.card.save()

        self.student_card = PropertyTemplate(name="学生卡", fields={"卡号": 1200, "颜色": 1}, type=self.card)
        self.student_card.save()

        self.bank_card = PropertyTemplate(name="银行卡", fields={"卡号": 10, "银行": 5}, type=self.card)
        self.bank_card.save()

        self.location_thu = {
                "name": "北京大学",
                "poiid": "City",
                "address": "北京市海淀区",
                "latitude": 40,
                "longitude": 116
            }

        self.location_pku = {
                "name": "北京大学",
                "poiid": "City",
                "address": "北京市海淀区",
                "latitude": 40,
                "longitude": 116
            }

        self.datetime1 = parse_datetime("2020-10-23T14:36:10.293102+08:00")
        self.datetime2 = parse_datetime("2020-11-24T14:36:10.293102+08:00")
        self.datetime3 = parse_datetime("2020-12-25T14:36:10.293102+08:00")
        self.datetime4 = parse_datetime("2020-12-26T14:36:10.293102+08:00")
        self.datetime5 = parse_datetime("2020-12-27T14:36:10.293102+08:00")


    def test_different_template(self):
        student_card = Property(name="李祁的学生卡", template=self.student_card, attributes={"卡号": "2017010256", "颜色": "黑色"})
        student_card.save()
        bank_card = Property(name="徐亦豪的银行卡", template=self.bank_card, attributes={"卡号": "2017010256", "银行": "农行"})
        bank_card.save()

        lost_notice = LostNotice.objects.create(property=student_card, author=self.user1, lost_location={"locations": [self.location_pku]}, est_lost_start_datetime=self.datetime1, est_lost_end_datetime=self.datetime2)
        lost_notice.save()
        found_notice = FoundNotice.objects.create(property=bank_card, author=self.user2, found_location=self.location_thu, found_datetime=self.datetime4)
        found_notice.save()

        matching_degree = matching(lost_notice=lost_notice, found_notice=found_notice)

        self.assertEqual(matching_degree, 0)


    def test_student_card_ID_matched(self):
        threshold = MatchingHyperParam.get_matching_threshold()

        student_card1 = Property(name="李祁的学生卡", template=self.student_card, attributes={"卡号": "2017010256", "颜色": "黑色"}, description="李祁的学生卡")
        student_card1.save()
        student_card2 = Property(name="徐亦豪的学生卡", template=self.student_card, attributes={"卡号": "2017010256", "颜色": "白色"}, description="一张学生卡")
        student_card2.save()

        lost_notice = LostNotice.objects.create(property=student_card1, author=self.user1, lost_location={"locations": [self.location_pku]}, est_lost_start_datetime=self.datetime1, est_lost_end_datetime=self.datetime4, description="在北馆丢失了一张学生卡")
        lost_notice.save()
        found_notice = FoundNotice.objects.create(property=student_card2, author=self.user2, found_location=self.location_thu, found_datetime=self.datetime5, description="在西操捡到了一张学生卡")
        found_notice.save()

        matching_degree = matching(lost_notice=lost_notice, found_notice=found_notice)

        self.assertGreater(matching_degree, threshold)

    def test_student_card_ID_unmatched(self):
        threshold = MatchingHyperParam.get_matching_threshold()

        student_card1 = Property(name="李祁的学生卡", template=self.student_card, attributes={"卡号": "2017010256", "颜色": "黑色"}, extra={'新旧': '新'})
        student_card1.save()
        student_card2 = Property(name="徐亦豪的学生卡", template=self.student_card, attributes={"卡号": "2017010255", "颜色": "黑色"}, extra={'新旧': '旧'})
        student_card2.save()

        lost_notice = LostNotice.objects.create(property=student_card1, author=self.user1, lost_location={"locations": [self.location_pku]},  est_lost_start_datetime=self.datetime1, est_lost_end_datetime=self.datetime1, extra={'什么时候': "星期一"})
        lost_notice.save()
        found_notice = FoundNotice.objects.create(property=student_card2, author=self.user2, found_location=self.location_thu, found_datetime=self.datetime5, extra={"什么时候": "星期二"})
        found_notice.save()

        matching_degree = matching(lost_notice=lost_notice, found_notice=found_notice)

        self.assertLess(matching_degree, threshold)

    def test_matching_notify(self):
        student_card1 = Property(name="李祁的学生卡", template=self.student_card, attributes={"卡号": "2017010256", "颜色": "黑色"})
        student_card1.save()
        student_card2 = Property(name="徐亦豪的学生卡", template=self.student_card, attributes={"卡号": "2017010256", "颜色": "白色"})
        student_card2.save()

        lost_notice = LostNotice.objects.create(property=student_card1, author=self.user1, lost_location={"locations": [self.location_pku]})
        lost_notice.save()
        found_notice = FoundNotice.objects.create(property=student_card2, author=self.user2, found_location=self.location_thu, found_datetime=self.datetime1)
        found_notice.save()

        matching_degree = matching(lost_notice=lost_notice, found_notice=found_notice)
        matching_entry = MatchingEntry.objects.create(lost_notice=lost_notice, found_notice=found_notice, matching_degree=matching_degree)
        matching_entry.save()

        response = self.client.post(f"/api/v1/matching-entries/{matching_entry.pk}/matching-notify/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f"/api/v1/matching-entries/{matching_entry.pk}/matching-notify/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)