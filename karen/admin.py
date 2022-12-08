from django.contrib import admin
from karen.models import Addon


class AddonAdmin(admin.ModelAdmin):
    list_display = (
        "upstream_url",
        "config_url",
    )


admin.site.register(Addon, AddonAdmin)