from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'estimated_time',
        'estimated_value',
        'value',
        'hours',
        'payment_date',
    )
