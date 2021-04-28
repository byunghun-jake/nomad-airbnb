from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import ListView
from django_countries import countries
from .models import Room, RoomType, Amenity, Facility, HouseRule
from .forms import SearchForm


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


def search(request):
    # 국가 정보가 없을 때 == 검색창을 통해 search 페이지로 들어온 경우
    country = request.GET.get("country")
    if country:
        # 입력 받은 내용을 Form에 넣는다.
        form = SearchForm(request.GET)
        # 유효성 검사
        if form.is_valid():
            # 정리된 데이터 (dict)를 추출한다.
            print(form.cleaned_data)
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            beds = form.cleaned_data.get("beds")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")
            is_instant_book = form.cleaned_data.get("is_instant_book")
            is_superhost = form.cleaned_data.get("is_superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            Q_city = Q(city__contains=city)
            if city == "근처 추천 장소":
                Q_city = Q(city__contains="")
            Q_country = Q(country__exact=country)
            Q_room_type = Q(room_type__exact=room_type)
            if room_type is None:
                Q_room_type = Q(room_type__isnull=False)
            Q_price = Q(price__lte=price)
            if price is None:
                Q_price = Q(price__lte=1000000000)
            Q_guests = Q(max_guests__gte=guests)
            if guests is None:
                Q_guests = Q(max_guests__gte=0)
            Q_beds = Q(beds__gte=beds)
            if beds is None:
                Q_beds = Q(beds__gte=0)
            Q_bedrooms = Q(bedrooms__gte=bedrooms)
            if bedrooms is None:
                Q_bedrooms = Q(bedrooms__gte=0)
            Q_baths = Q(baths__gte=baths)
            if baths is None:
                Q_baths = Q(baths__gte=0)
            Q_instant_book = Q(instant_book__exact=is_instant_book)
            Q_is_superhost = Q(host__is_superhost__isnull=False)
            if is_superhost:
                Q_is_superhost = Q(host__is_superhost__exact=True)
            # Q_amenities = Q(amenities__in=amenities)
            # Q_facilities = Q(facilities__in=facilities)

            qs = Room.objects.filter(
                Q_city
                & Q_country
                & Q_room_type
                & Q_price
                & Q_guests
                & Q_beds
                & Q_bedrooms
                & Q_baths
                & Q_instant_book
                & Q_is_superhost
            )

    else:
        # 도시를 입력하지 않았을 때,
        if request.GET.get("city", "") == "":
            form = SearchForm()
            qs = Room.objects.filter(country__exact="KR")
        else:
            # 렌더링을 위해 빈 폼을 넣는다.
            # 도시를 검색했는데, 빈 폼을 넣는다는 것도 잘 이해가 안가긴 함
            # 대한민국을 기본값으로 하려면?
            request.GET = request.GET.copy()
            request.GET["country"] = "KR"
            form = SearchForm(request.GET)
            city = request.GET.get("city")
            country = "KR"
            qs = Room.objects.filter(city__contains=city, country__exact=country)
    paginator = Paginator(qs, 10, allow_empty_first_page=True)
    page = int(request.GET.get("page", 1))
    rooms = paginator.get_page(page)

    context = {
        "form": form,
        "rooms": rooms,
    }
    return render(request, "rooms/search.html", context)