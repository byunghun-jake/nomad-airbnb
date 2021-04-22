from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "시설을 생성하기 위한 코드"

    def handle(self, *args, **kwargs):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        count = 0
        for facility in facilities:
            try:
                Facility.objects.get(name=facility)
            except:
                Facility.objects.create(name=facility)
                count += 1
        else:
            print(f"{count}개의 시설을 추가하였습니다.")
