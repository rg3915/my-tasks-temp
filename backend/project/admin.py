from django.contrib import admin

from .models import Owner, Project


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'repository_name')
    search_fields = ('title', 'customer__name', 'repository_name')
    list_filter = ('active', 'customer', 'repository_owner')
