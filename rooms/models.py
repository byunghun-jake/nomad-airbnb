from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from core.models import TimeStampedModel

# 다른 아이템들(RoomType, Facilities, Rules)을 생성하기 위한 모델 클래스
class AbstractItem(TimeStampedModel):
    """ AbstractItem """

    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Room(TimeStampedModel):

    """ Room Model definition """

    # 1(User):N(Room)
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # items
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    house_rules = models.ManyToManyField(HouseRule)

    name = models.CharField(max_length=140)
    description = models.TextField()
    # 국가 정보를 위해 서드파티 라이브러리 설치
    country = CountryField()
    city = models.CharField(max_length=140)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    max_guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = self.city.title()
        super().save(*args, **kwargs)

    def total_rating(self):
        reviews = self.review_set.all()
        if reviews:
            total_score = 0
            review_count = len(reviews)
            for review in reviews:
                total_score += review.average_score()
            return round(total_score / review_count, 2)
        else:
            return 0


class Photo(TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    # 밑에 정의되어 있어, String으로 입력
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption