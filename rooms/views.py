from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
from .models import Room


def index(request):
    # 모든 방 정보를 불러온다.
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, "rooms/index.html", context)