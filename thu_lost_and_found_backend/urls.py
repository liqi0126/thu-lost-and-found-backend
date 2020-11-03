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
from thu_lost_and_found_backend.user_service.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'property-types', PropertyTypeViewSet)
router.register(r'property-templates', PropertyTemplateViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'found-notices', FoundNoticeViewSet)
router.register(r'lost-notices', LostNoticeViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]

# image links
# if /media/ is defined as the MEDIA_URL, the below statements are needed
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
