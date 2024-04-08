from django.contrib import admin
from .models import Vendor, Container, Log, FinishedLog

# Register your models here.
admin.site.register(Vendor)
@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("id","container_number", "pieces", "vendor")
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id","container", "cft", "cbm")
@admin.register(FinishedLog)
class FinishedLogAdmin(admin.ModelAdmin):
    list_display = ("id","log", "length", "width", "thickness")