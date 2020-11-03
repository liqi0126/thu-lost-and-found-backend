from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from thu_lost_and_found_backend.property_service.views import PropertyTypeViewSet, PropertyTemplateViewSet, \
    PropertyViewSet

router = routers.DefaultRouter()
router.register(r'property-types', PropertyTypeViewSet)
router.register(r'property-templates', PropertyTemplateViewSet)
router.register(r'properties', PropertyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]

# image links
# if /media/ is defined as the MEDIA_URL, the below statements are needed
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
