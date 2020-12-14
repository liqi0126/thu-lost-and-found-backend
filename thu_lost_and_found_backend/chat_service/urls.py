# chat/urls.py
from django.urls import path

from . import views

# TODO: temp file for debug
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]