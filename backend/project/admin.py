from django.contrib import admin
from import_export import resources

from .models import Owner, Project


class OwnerResource(resources.ModelResource):
    class Meta:
        model = Owner


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    resource_classes = (OwnerResource,)
    list_display = ('__str__',)
    search_fields = ('name',)


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    resource_classes = (ProjectResource,)
    list_display = ('__str__', 'customer', 'repository_name')
    search_fields = ('title', 'customer__name', 'repository_name')
    list_filter = ('active', 'customer', 'repository_owner')
