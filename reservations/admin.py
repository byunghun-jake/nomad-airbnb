from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "guest",
        "status",
        "check_in",
        "check_out",
        "is_in_progress",
        "is_finished",
    )

    list_filter = ("status",)


admin.site.register(Reservation, ReservationAdmin)