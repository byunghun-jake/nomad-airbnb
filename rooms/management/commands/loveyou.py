from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command tells me that I love you"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I love you?"
        )

    def handle(self, *args, **options):
        times = options.get("times")
        for _ in range(int(times)):
            print("Love you")