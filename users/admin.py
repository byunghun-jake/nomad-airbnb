from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from rooms.models import Room


class RoomInline(admin.StackedInline):
    model = Room


class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "CustomProfile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "is_superhost",
                ),
            },
        ),
    )

    inlines = (RoomInline,)

    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "language",
        "currency",
        "is_active",
        "is_staff",
        "is_superhost",
        "is_superuser",
    ]

    list_filter = UserAdmin.list_filter + (
        "language",
        "currency",
        "is_superhost",
    )


admin.site.register(get_user_model(), CustomUserAdmin)
