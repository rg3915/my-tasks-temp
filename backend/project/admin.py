from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'repository_name')
    search_fields = ('title', 'customer__name', 'repository_name')
    list_filter = ('active', 'customer')
