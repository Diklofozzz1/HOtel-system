from django.contrib import admin

import client.models as model


# Register your models here.

@admin.register(model.Order)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "client_id", "phone_number")
    pass


@admin.register(model.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "second_name", "passport_field")
    pass


@admin.register(model.BlackList)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "client_id")
    pass
