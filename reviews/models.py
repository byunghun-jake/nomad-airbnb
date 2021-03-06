from django.db import models
from django.conf import settings
from core.models import TimeStampedModel


class Review(TimeStampedModel):

    """ Review Model Definition """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    content = models.TextField()
    # score
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return f"{self.content} - {self.room.name}"

    def average_score(self):
        score = (
            sum(
                [
                    self.accuracy,
                    self.communication,
                    self.cleanliness,
                    self.location,
                    self.check_in,
                    self.value,
                ]
            )
            / 6
        )

        # return f"{score:.2f}"
        return round(score, 2)
