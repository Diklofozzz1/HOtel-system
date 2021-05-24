from django.db import models

from hotel_numbers.models import HotelNumber
from reg.models import Worker


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=16, default='')
    second_name = models.CharField(max_length=16, default='')
    third_name = models.CharField(max_length=16, default='')
    date = models.DateField(default='')
    passport_field = models.CharField(max_length=10, default='', unique='True')

    def __str__(self):
        return self.first_name + ' ' + self.second_name + ' ' + self.third_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    check_in_date = models.DateField(default='')
    check_out_date = models.DateField(default='')
    phone_number = models.CharField(max_length=16, default='')
    complementary_services = models.CharField(max_length=50, default='')
    execution = models.BooleanField(default=False)
    executed = models.BooleanField(default=False)
    room_number = models.PositiveIntegerField(default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    number = models.ForeignKey(HotelNumber, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.second_name + ' ' + self.client.third_name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class BlackList(models.Model):
    case_date = models.DateField(auto_now_add=True)
    time_out_date = models.DateField(default='')
    reason = models.CharField(max_length=200, default='', null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.second_name + ' ' + self.client.third_name

    class Meta:
        verbose_name = 'Черный список'


class ServiceList(models.Model):
    name = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справочник доп. услуг'


class MenuList(models.Model):
    menu = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.menu

    class Meta:
        verbose_name = 'Меню'


class AdditionalOrder(models.Model):
    order_date = models.DateField(default='')
    coast = models.FloatField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(ServiceList, on_delete=models.CASCADE, null=True)
    Menu = models.ForeignKey(MenuList, on_delete=models.CASCADE, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.service.name + ' ' + self.client.first_name + ' ' + self.client.second_name + ' ' + self.client.third_name

    class Meta:
        verbose_name = 'Заказ (дополнительные услуги)'
        verbose_name_plural = 'Заказы (дополнительные услуги)'
