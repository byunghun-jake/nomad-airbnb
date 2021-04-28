from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.room_set.count()


class PhotoInline(admin.TabularInline):

    """ RoomAdmin에 Photo를 넣기위한 클래스 """

    model = Photo


class RoomAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    fieldsets = (
        (
            "기본 정보",
            {
                "fields": (
                    "host",
                    "name",
                    "room_type",
                    "description",
                    "country",
                    "city",
                    "price",
                    "address",
                    "instant_book",
                )
            },
        ),
        (
            "시간",
            {
                "fields": (
                    "check_in",
                    "check_out",
                )
            },
        ),
        (
            "공간",
            {
                "fields": (
                    "beds",
                    "bedrooms",
                    "baths",
                    "max_guests",
                )
            },
        ),
        (
            "공간 세부정보",
            {
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                )
            },
        ),
    )

    raw_id_fields = ("host",)

    inlines = (PhotoInline,)

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "max_guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__is_superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = [
        "city",
        "name",
        "host__username",
    ]

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    ordering = (
        "name",
        "country",
    )

    # def save_model(self, request, obj, form, change):
    #     obj.city = obj.city.title()
    #     return super().save_model(request, obj, form, change)

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photo_set.count()

    count_amenities.short_description = "amenity count"
    count_photos.short_description = "photo count"


class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f"<img style='height: 50px;' src='{obj.file.url}' />")

    get_thumbnail.short_description = "Tumbnail"


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, ItemAdmin)
admin.site.register(Amenity, ItemAdmin)
admin.site.register(Facility, ItemAdmin)
admin.site.register(HouseRule, ItemAdmin)
admin.site.register(Photo, PhotoAdmin)