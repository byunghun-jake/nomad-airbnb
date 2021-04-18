from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel


class List(TimeStampedModel):

    """ List Model Definition """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rooms = models.ManyToManyField("rooms.Room", blank=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} by. {self.user.username}"

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "Number of Rooms"