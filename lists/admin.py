from django.contrib import admin
from .models import List


class ListAdmin(admin.ModelAdmin):

    """ List Admin Definition """

    list_display = (
        "name",
        "user",
        "count_rooms",
    )

    search_fields = (
        "name",
        "user__username",
    )


admin.site.register(List, ListAdmin)