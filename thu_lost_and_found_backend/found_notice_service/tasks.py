from celery import shared_task

from .models import FoundNotice
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice, LostNoticeStatus
from thu_lost_and_found_backend.matching_service.models import MatchingEntry
from thu_lost_and_found_backend.matching_service.match import matching, MATCHING_THRESHOLD
from thu_lost_and_found_backend.matching_service.notify import matching_notify


@shared_task
def create_matching_task(found_notice_id):
    found_notice = FoundNotice.objects.get(pk=found_notice_id)
    lost_notices = LostNotice.objects.filter(status=LostNoticeStatus.PUBLIC,
                                             property__template=found_notice.property.template)
    just_sent_users = []
    for lost_notice in lost_notices:
        matching_degree = matching(lost_notice, found_notice)
        matching_entry = MatchingEntry.objects.create(lost_notice=lost_notice, found_notice=found_notice,
                                                      matching_degree=matching_degree)
        matching_entry.save()
        # try to notify user
        if matching_degree > MATCHING_THRESHOLD:
            matching_notify(matching_entry, just_sent=lost_notice.author.id in just_sent_users)
            just_sent_users.append(lost_notice.author.id)


@shared_task
def update_matching_task(found_notice_id):
    found_notice = FoundNotice.objects.get(pk=found_notice_id)
    just_sent_users = []
    for matching_entry in MatchingEntry.objects.filter(found_notice=found_notice):
        lost_notice = matching_entry.lost_notice
        matching_degree = matching(lost_notice, found_notice)
        matching_entry.matching_degree = matching_degree
        matching_entry.save()
        # try to notify user
        if matching_degree > MATCHING_THRESHOLD:
            matching_notify(matching_entry, lost_notice.author.id in just_sent_users)
            just_sent_users.append(lost_notice.author.id)