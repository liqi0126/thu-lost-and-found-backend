from rest_framework import viewsets

from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.user_service.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
