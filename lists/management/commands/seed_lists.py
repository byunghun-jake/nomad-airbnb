import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from rooms.models import Room


class Command(BaseCommand):
    help = "방을 저장하는 리스트를 만드는 씨드입니다."

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="리스트를 몇 개 만들까요?")

    def handle(self, *args, **options):
        users = get_user_model().objects.all()
        rooms = Room.objects.all()
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            List,
            number,
            {
                "user": lambda x: random.choice(users),
                "name": lambda x: seeder.faker.name(),
            },
        )
        new_lists = seeder.execute()
        list_pk_list = flatten(new_lists.values())
        for list_pk in list_pk_list:
            new_list = List.objects.get(pk=list_pk)
            room_in_list = random.sample(list(rooms), k=random.randint(3, 8))
            new_list.rooms.add(*room_in_list)
        print(f"{number}개의 리스트를 만들었습니다.")