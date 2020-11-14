from rest_framework import viewsets

from thu_lost_and_found_backend.authentication_service.models import UserVerificationApplication
from thu_lost_and_found_backend.authentication_service.serializer import UserVerificationApplicationSerializer


class UserVerificationApplicationViewSet(viewsets.ModelViewSet):
    queryset = UserVerificationApplication.objects.all()
    serializer_class = UserVerificationApplicationSerializer
