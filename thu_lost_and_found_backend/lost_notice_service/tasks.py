from celery import shared_task

from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice, FoundNoticeStatus
from thu_lost_and_found_backend.matching_service.models import MatchingEntry
from thu_lost_and_found_backend.matching_service.match import matching

@shared_task
def create_matching_task(lost_notice_id):
    lost_notice = LostNotice.objects.get(pk=lost_notice_id)
    found_notices = FoundNotice.objects.filter(status=FoundNoticeStatus.PUBLIC, property__template=lost_notice.property.template)
    for found_notice in found_notices:
        matching_degree = matching(lost_notice, found_notice)
        matching_entry = MatchingEntry.objects.create(lost_notice=lost_notice, found_notice=found_notice, matching_degree=matching_degree)
        matching_entry.save()


@shared_task
def update_matching_task(lost_notice_id):
    lost_notice = LostNotice.objects.get(pk=lost_notice_id)
    for matching_entry in MatchingEntry.objects.filter(lost_notice=lost_notice):
        matching_degree = matching(lost_notice, matching_entry.found_notice)
        matching_entry.matching_degree = matching_degree
        matching_entry.save()
