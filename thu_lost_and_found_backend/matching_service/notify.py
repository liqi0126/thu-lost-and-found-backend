from django.core.mail import send_mail

from thu_lost_and_found_backend import settings
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice

from .email_matched_notify_template import email_matched_notify_template

MATCHING_THRESHOLD = 0.8


def matching_notify(lost_notice: LostNotice):

    if lost_notice.author.email is not None:
        send_mail(subject='失物匹配提示',
                  message='',
                  html_message=email_matched_notify_template.format(
                    object=lost_notice.property.name
                  ),

                  from_email=f'"{settings.EMAIL_DISPLAY_NAME}" <{settings.EMAIL_HOST_USER}>',
                  recipient_list=[lost_notice.author.email],
                  fail_silently=False)

    # TODO: cannot send SMS without business license ...
    if lost_notice.author.phone is not None:
        pass

    # TODO: cannot send wechat notice without business license ...
    if lost_notice.author.wechat_id is not None:
        pass
