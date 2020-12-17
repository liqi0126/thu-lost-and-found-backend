import json

from django.core.mail import send_mail

from thu_lost_and_found_backend import settings
from thu_lost_and_found_backend.matching_service.models import MatchingEntry
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.chat_service.consumers import ChatConsumer

from .email_matched_notify_template import email_matched_notify_template


def matching_notify(matching_entry: MatchingEntry, just_sent=False):

    lost_notice = matching_entry.lost_notice
    found_notice = matching_entry.found_notice
    matching_degree = matching_entry.matching_degree

    # message in wechat mini program
    admin_consumer = ChatConsumer()
    admin_consumer.send_message(1, lost_notice.author.id, json.dumps({
        "lost_notice": lost_notice.id,
        "found_notice": found_notice.id,
        "matching_degree": matching_degree
    }))

    if lost_notice.author.email is not None and not just_sent:
        send_mail(subject='失物匹配提示',
                  message='',
                  html_message=email_matched_notify_template.format(
                    object=lost_notice.property.name
                  ),

                  from_email=f'"{settings.EMAIL_DISPLAY_NAME}" <{settings.EMAIL_HOST_USER}>',
                  recipient_list=[lost_notice.author.email],
                  fail_silently=False)

    # TODO: cannot send SMS without business license ...
    if lost_notice.author.phone is not None and not just_sent:
        pass

    # TODO: cannot send wechat notice without business license ...
    if lost_notice.author.wechat_id is not None and not just_sent:
        pass
