from django.contrib import admin

from .models import Container, FinishedLog, Log, Vendor

admin.site.site_header = 'Admin Dashboard'
admin.site.index_title = 'Woods Logs Recode App'
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
