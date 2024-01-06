from django.contrib import admin
from import_export import resources

from .models import Payment


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    resource_classes = (PaymentResource,)
    list_display = (
        '__str__',
        'estimated_time',
        'estimated_value',
        'value_per_hour',
        'value_total',
        'spent_time_total',
        'payment_date',
    )
