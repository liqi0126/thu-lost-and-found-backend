from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from thu_lost_and_found_backend.contact_service.views import ContactViewSet
from thu_lost_and_found_backend.found_notice_service.views import FoundNoticeViewSet
from thu_lost_and_found_backend.lost_notice_service.views import LostNoticeViewSet
from thu_lost_and_found_backend.property_service.views import PropertyTypeViewSet, PropertyTemplateViewSet, \
    PropertyViewSet
from thu_lost_and_found_backend.tag_service.views import TagViewSet
from thu_lost_and_found_backend.user_service.views import UserViewSet, UserInvitationViewSet, \
    UserEmailVerificationViewSet, UserVerificationApplicationViewSet

router = routers.DefaultRouter()
router.register(r'property-types', PropertyTypeViewSet)
router.register(r'property-templates', PropertyTemplateViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'tags', TagViewSet)
router.register(r'found-notices', FoundNoticeViewSet)
router.register(r'lost-notices', LostNoticeViewSet)
router.register(r'users', UserViewSet)
router.register(r'user-invitations', UserInvitationViewSet)
router.register(r'user-email-verifications', UserEmailVerificationViewSet)
router.register(r'user-verification-applications', UserVerificationApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('thu_lost_and_found_backend.authentication_service.urls'))
]

# image links
# if /media/ is defined as the MEDIA_URL, the below statements are needed
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
