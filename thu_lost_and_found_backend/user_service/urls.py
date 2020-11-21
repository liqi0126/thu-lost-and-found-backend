from django.urls import path

from . import views

urlpatterns = [
    path('user-invitations/register/<slug:token>/', views.UserInvitationViewSet.register),
]
