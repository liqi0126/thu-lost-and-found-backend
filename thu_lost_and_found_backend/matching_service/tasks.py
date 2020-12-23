from celery import shared_task

from thu_lost_and_found_backend.lost_notice_service.models import LostNotice, LostNoticeStatus
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice, FoundNoticeStatus

from .models import MatchingEntry
from .match import matching
from .notify import matching_notify


@shared_task
def update_matching_task(template_id=None):
    if template_id is None:
        lost_notices = LostNotice.objects.filter(status=LostNoticeStatus.PUBLIC)
    else:
        lost_notices = LostNotice.objects.filter(status=LostNoticeStatus.PUBLIC, property__template=template_id)

    for lost_notice in lost_notices:
        for found_notice in FoundNotice.objects.filter(property__template=lost_notice.property.template, status=FoundNoticeStatus.PUBLIC):
            matching_degree = matching(lost_notice, found_notice)
            try:
                matching_entry = MatchingEntry.objects.get(lost_notice=lost_notice, found_notice=found_notice)
            except MatchingEntry.DoesNotExist:
                matching_entry = MatchingEntry.objects.create(lost_notice=lost_notice, found_notice=found_notice)
            matching_entry.matching_degree = matching_degree
            matching_entry.save()

            matching_notify(matching_entry)
