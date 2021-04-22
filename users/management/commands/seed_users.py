from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_seed import Seed


class Command(BaseCommand):
    help = "가짜 이용자를 만들기 위한 커맨드"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="몇 명의 유저를 생성하시겠습니까?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # 세번째 인자로 특별히 다룰 컬럼에 대한 설정을 해줍니다.
        seeder.add_entity(
            get_user_model(),
            number,
            {
                "is_staff": False,
                "is_superuser": False,
            },
        )
        # 생성한 seeder를 실행합니다.
        seeder.execute()
        print(f"{number}명의 유저를 추가하였습니다.")
