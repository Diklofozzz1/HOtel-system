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
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True)
    number_type = models.ForeignKey(NumberType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.number_type.name


class Storage(models.Model):
    name = models.CharField(max_length=50, default='')
    coast = models.FloatField(null=True)
    quantity = models.IntegerField(default=0)
    dirty_staff = models.IntegerField(default=0)
    condition = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RoomDecoration(models.Model):
    number = models.ForeignKey(HotelNumber, on_delete=models.PROTECT, null=True)
    article = models.ForeignKey(Storage, on_delete=models.PROTECT, null=True)


class WashHouse(models.Model):
    number = models.IntegerField(default=0)
    condition = models.BooleanField(default=False)
    coast = models.FloatField(null=True)
    article = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True)


class Provider(models.Model):
    name = models.CharField(max_length=15, default='', null=True)
    phone_number = models.CharField(max_length=20, default='', unique='True')


class StaffOrder(models.Model):
    name = models.CharField(max_length=200, default='', null=True)
    coast = models.FloatField(null=True)
    order_date = models.DateField(auto_now_add=True)
    count = models.IntegerField(default=0)
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
