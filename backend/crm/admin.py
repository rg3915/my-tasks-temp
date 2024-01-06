from django.contrib import admin
from import_export import resources

from .models import Customer


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    resource_classes = (CustomerResource,)
    list_display = ('__str__',)
    search_fields = ('name',)
    list_filter = ('active',)
