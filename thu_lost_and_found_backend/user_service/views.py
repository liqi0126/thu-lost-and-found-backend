from rest_framework import viewsets
from rest_framework.response import Response

from thu_lost_and_found_backend.helpers.toolkits import delete_media_instance
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.user_service.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, pk=None):
        delete_media_instance(User, pk, 'avatar')
        return Response(status=204)
