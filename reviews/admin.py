from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    list_display = (
        "__str__",
        "user",
        "average_score",
    )


admin.site.register(Review, ReviewAdmin)