from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if phone_number is None:
            raise TypeError("Username cannot be blank")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError("Enter password")
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class Worker(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=16, default='')
    second_name = models.CharField(max_length=16, default='')
    third_name = models.CharField(max_length=16, default='')
    address_name = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='', unique='True')
    password = models.CharField(max_length=255, default='')
    positions = models.ForeignKey('Positions', on_delete=models.PROTECT, null=True)
    bonuses = models.FloatField(null=True)
    fine = models.FloatField(null=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    last_login = None
    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.second_name + ' ' + self.third_name

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class Positions(models.Model):
    name = models.CharField(max_length=15, default='')
    payment = models.FloatField(null=True)
    insurance = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Vacation(models.Model):
    date_start = models.DateField(default='')
    date_end = models.DateField(default='')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.worker.first_name + ' ' + self.worker.second_name + ' ' + self.worker.third_name

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'


def __str__(self):
    return self.username