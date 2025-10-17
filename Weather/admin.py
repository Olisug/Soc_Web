from django.contrib import admin
from Weather.models import Apps


@admin.register(Apps)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('app_name',)
    search_fields = ('app_name',)
