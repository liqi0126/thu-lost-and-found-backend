from rest_framework import viewsets
from rest_framework.response import Response

from thu_lost_and_found_backend.helpers.toolkits import delete_instance_medias
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.user_service.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'avatar')
        instance.delete()
