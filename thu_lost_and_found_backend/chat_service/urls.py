# chat/urls.py
from django.urls import path

from . import views

# TODO: temp file for debug
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user_id>/', views.room, name='room'),
]