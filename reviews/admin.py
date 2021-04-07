from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    pass


admin.site.register(Review, ReviewAdmin)