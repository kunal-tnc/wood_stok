from django.contrib import admin

from .models import *

admin.site.site_header = "Admin Dashboard"
admin.site.index_title = "Woods Logs Recode App"
admin.site.register(Vendor)


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("id", "container_number", "pieces", "vendor")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "container", "cft", "cbm")


@admin.register(FinishedLog)
class FinishedLogAdmin(admin.ModelAdmin):
    list_display = ("id", "log", "length", "width", "thickness")


@admin.register(SaleOrderline)
class SaleOrderlineAdmin(admin.ModelAdmin):
    list_display = ("id", "width", "thickness", "quantity")


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "sale_date", "width", "thickness", "length", "quantity")

    def width(self, obj):
        return obj.orderline.width

    def thickness(self, obj):
        return obj.orderline.thickness

    def length(self, obj):
        return obj.orderline.length

    def quantity(self, obj):
        return obj.orderline.quantity

    width.short_description = "Width"
    thickness.short_description = "Thickness"
    length.short_description = "Length"
    quantity.short_description = "Quantity"
