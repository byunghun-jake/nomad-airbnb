from django import forms
from django_countries.fields import CountryField
from .models import Room, RoomType, Amenity, Facility


class SearchForm(forms.Form):
    city = forms.CharField(initial="근처 추천 장소")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        empty_label="모든 방", queryset=RoomType.objects.all(), required=False
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    is_instant_book = forms.BooleanField(required=False)
    is_superhost = forms.BooleanField(required=False)
    # amenities = forms.ModelMultipleChoiceField(
    #     required=False,
    #     queryset=Amenity.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )
    # facilities = forms.ModelMultipleChoiceField(
    #     required=False,
    #     queryset=Facility.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )
