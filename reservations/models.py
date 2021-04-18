from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel


class Reservation(TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "예약 진행 중"),
        (STATUS_CONFIRMED, "예약 확정"),
        (STATUS_CANCELED, "예약 취소"),
    )

    # 사람은 여러 예약을 만들 수 있지
    guest = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # 한 방을 기준으로 여러 예약이 생성될 수 있어
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    # 예약 날짜
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - {self.check_in} / {self.check_out}"

    def is_in_progress(self):
        # 현재 시간과 체크인, 체크아웃 시간을 비교한다.
        today = timezone.now().date()
        return self.check_in <= today <= self.check_out

    is_in_progress.boolean = True

    def is_finished(self):
        today = timezone.now().date()
        return self.check_out < today

    is_finished.boolean = True