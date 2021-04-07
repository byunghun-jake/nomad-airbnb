from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    pass


admin.site.register(Reservation, ReservationAdmin)