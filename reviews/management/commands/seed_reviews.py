import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from rooms.models import Room


class Command(BaseCommand):
    help = "방에 대한 리뷰를 생성하는 시드입니다."

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="리뷰를 몇개 생성할까?")

    def handle(self, *args, **options):
        users = get_user_model().objects.all()
        rooms = Room.objects.all()
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            Review,
            number,
            {
                "user": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "content": lambda x: seeder.faker.paragraph(),
                "accuracy": lambda x: random.randint(3, 5),
                "communication": lambda x: random.randint(3, 5),
                "cleanliness": lambda x: random.randint(3, 5),
                "location": lambda x: random.randint(3, 5),
                "check_in": lambda x: random.randint(3, 5),
                "value": lambda x: random.randint(3, 5),
            },
        )
        seeder.execute()
        print(f"{number}개의 리뷰가 생성되었습니다.")
