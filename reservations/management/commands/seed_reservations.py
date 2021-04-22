import random
import datetime
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_seed import Seed
from rooms.models import Room
from reservations.models import Reservation

STATUS = (
    "pending",
    "confirmed",
    "canceled",
)


class Command(BaseCommand):
    help = "더미 예약을 만들기 위한 명령어"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="몇 개의 예약을 생성할지 결정하세요."
        )

    def handle(self, *args, **options):
        users = get_user_model().objects.all()
        rooms = Room.objects.all()
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            Reservation,
            number,
            {
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                # Status(SelectField)는 어떻게 할까?
                "status": lambda x: random.choice(STATUS),
                "check_in": lambda x: timezone.now().date(),
                "check_out": lambda x: timezone.now().date()
                + datetime.timedelta(days=random.randint(4, 20)),
            },
        )
        seeder.execute()
        print(f"{number}개의 예약이 생성되었습니다.")
