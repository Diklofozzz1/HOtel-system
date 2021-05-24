from django.contrib import admin

import reg.models as model


# Register your models here.

@admin.register(model.Worker)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "second_name", "phone_number")
    pass


@admin.register(model.Positions)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    pass


@admin.register(model.Vacation)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "date_start")
    pass
