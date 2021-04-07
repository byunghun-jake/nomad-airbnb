from django.contrib import admin
from .models import Conversation, Message


class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    pass


class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)