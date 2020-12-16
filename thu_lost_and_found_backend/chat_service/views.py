# chat/views.py
from django.shortcuts import render

# TODO: temp file for debug
def index(request):
    return render(request, 'chat/index.html', {})


def room(request, user_id):
    return render(request, 'chat/room.html', {
        'user_id': user_id
    })