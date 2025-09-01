from django.contrib import admin
from .models import Project, Skill, ContactMessage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "proficiency_level")
    list_filter = ("proficiency_level",)
    search_fields = ("name",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email")
    readonly_fields = ("name", "email", "message", "submitted_at")
