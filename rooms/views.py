from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Room


def index(request):
    page = int(request.GET.get("page", 1))
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 10)
    try:
        pages = paginator.page(page)
        context = {
            "pages": pages,
        }
        return render(request, "rooms/index.html", context)
    except:
        return redirect("rooms:index")


def detail(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    context = {
        "room": room,
    }
    return render(request, "rooms/detail.html", context)