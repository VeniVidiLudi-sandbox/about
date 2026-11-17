from django.contrib import admin

from .models import Heartbeat, Profile, Project, Technology

admin.site.register(Profile)
admin.site.register(Heartbeat)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "published")
    list_editable = ("order", "published")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("technologies",)
