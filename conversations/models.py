from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel


class Conversation(TimeStampedModel):

    """ Conversation Model Definition """

    # 대화에 참여하는 사람은 여러명(3명 이상)이 될 수 있다.
    participants = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        username_list = []
        participants = self.participants.all()
        for participant in participants:
            username_list.append(participant.username)
        return ", ".join(username_list)

    def count_participants(self):
        return self.participants.count()


# 대화에서 사용되는 메세지를 만드는 클래스
class Message(TimeStampedModel):

    """ Message Model Definition """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.content}"