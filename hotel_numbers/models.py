from django.db import models

from reg.models import Worker


class NumberType(models.Model):
    name = models.CharField(max_length=45, default='')
    coast = models.FloatField(null=True)
    number_of_room = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class HotelNumber(models.Model):
    number_of_residents = models.IntegerField(default=0)
    coast_per_day = models.FloatField(null=True)
    room_occupancy = models.BooleanField(default=False)
    room_condition = models.BooleanField(default=True)
    complementary_services = models.CharField(max_length=50, default='')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
    number_type = models.ForeignKey(NumberType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.number_type.name
