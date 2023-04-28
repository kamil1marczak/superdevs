from django.contrib import admin

from superdevs.starwars.models import Dataset


class DatasetAdmin(admin.ModelAdmin):
    list_display = ["path", "is_deleted", "created_at", "updated_at"]


admin.site.register(Dataset, DatasetAdmin)
