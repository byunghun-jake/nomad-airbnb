from django.contrib import admin
from .models import Conversation, Message


class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    list_display = (
        "__str__",
        "count_participants",
    )

    filter_horizontal = ("participants",)


class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    list_display = (
        "__str__",
        "created_at",
    )


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)