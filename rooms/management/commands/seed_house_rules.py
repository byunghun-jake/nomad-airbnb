from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):
    help = "규칙을 생성하기 위한 시드"

    def handle(self, *args, **kwargs):
        house_rules = [
            "No smoking.",
            "No parties or events.",
            "No pets/Pets allowed.",
            "No unregistered guests.",
            "No food or drink in bedrooms.",
            "No loud noise after 11 PM.",
        ]
        count = 0
        for house_rule in house_rules:
            try:
                HouseRule.objects.get(name=house_rule)
            except:
                count += 1
                HouseRule.objects.create(name=house_rule)
        print(f"{count}개의 규칙을 생성했습니다.")