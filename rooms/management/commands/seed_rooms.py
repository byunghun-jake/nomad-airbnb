import random
from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_seed import Seed
from rooms.models import Room, RoomType, Amenity, Facility, HouseRule, Photo


class Command(BaseCommand):
    help = "가짜 방을 생성하기 위한 커맨드"

    def add_arguments(self, parser):
        # 첫 번째 인자: 어떤 문자를 argument 신호로 줄 지
        parser.add_argument("--number", default=1, type=int, help="얼마나 많은 방을 생성할까요?")

    def handle(self, *args, **options):
        number = options.get("number")
        # Room의 Foreign Key를 위해 연결된 모델을 불러옵니다.
        users = get_user_model().objects.all()[:25]
        room_types = RoomType.objects.all()
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        house_rules = HouseRule.objects.all()

        # seeder 인스턴스를 생성합니다.
        seeder = Seed.seeder()
        # seeder에 어떤 걸 생성하고 싶은지 추가합니다.
        # entity: 실체, 객체
        # 첫 번째 인자로 어떤 모델에 대한 객체인지 알려줍니다.
        # 두 번째 인자로 몇 개의 객체를 생성할지 알려줍니다.
        # 세 번째 인자로 모델의 컬럼을 직접 커스텀하고 싶은 내용을 전달합니다.
        # key(컬럼) - value(들어갈 값)
        # 모델끼리 연결된 경우(ForeignKey) 세 번째 인자로 지정해주어야 합니다.
        seeder.add_entity(
            Room,
            number,
            {
                "name": lambda x: seeder.faker.company(),
                "host": lambda x: random.choice(users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(100, 2000),
                "beds": lambda x: random.randint(0, 10),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(1, 6),
                "max_guests": lambda x: random.randint(1, 20),
            },
        )

        # seeder를 실행합니다.
        # 생성한 room 객체를 변수에 담습니다.
        # 여러 방을 생성한 경우 방 목록이 담깁니다.
        new_room = seeder.execute()
        # print(room)
        # print(flatten(new_room.values()))
        for room_pk in flatten(new_room.values()):
            room = Room.objects.get(pk=room_pk)
            # room의 사진 추가
            for _ in range(3, random.randint(5, 10)):
                Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"/room_photos/{random.randint(1, 31)}.webp",
                    room=room,
                )
            # amenity 추가
            for amenity in amenities:
                if random.randint(0, 1):
                    room.amenities.add(amenity)
            # facility 추가
            for facility in facilities:
                if random.randint(0, 1):
                    room.facilities.add(facility)
            # house_rule 추가
            for house_rule in house_rules:
                if random.randint(0, 1):
                    room.house_rules.add(house_rule)

        print(f"{number}개의 방을 생성했습니다.")