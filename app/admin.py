from django.contrib import admin
from .models import Content, Channel, ContentDetails


class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "slug",)
    list_editable = ("is_active",)
    search_fields = ("title", "description",)
    readonly_fields = ("slug",)
    list_filter = ("channel", "is_active")


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    search_fields = ("name",)
    readonly_fields = ("slug",)


class ContentDetailsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "slug",)
    list_editable = ("is_active",)
    search_fields = ("title", "description_detail",)
    readonly_fields = ("slug",)
    list_filter = ("cont", "is_active")


admin.site.register(Content, ContentAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(ContentDetails, ContentDetailsAdmin)
