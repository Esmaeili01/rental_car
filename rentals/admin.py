from django.contrib import admin
from django.utils.html import format_html
from .models import Rental

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['rental_id', 'customer', 'car', 'pickup_date', 'return_date', 'status', 'total_amount', 'is_overdue']
    list_filter = ['status', 'pickup_date', 'return_date', 'car__brand', 'car__category']
    search_fields = ['rental_id', 'customer__user__username', 'customer__user__email', 'car__license_plate', 'car__brand__name']
    list_editable = ['status']
    readonly_fields = ['rental_id', 'subtotal', 'total_amount', 'total_days', 'created_at', 'updated_at']
    date_hierarchy = 'pickup_date'
    
    fieldsets = (
        ('Rental Information', {
            'fields': ('rental_id', 'customer', 'car', 'status')
        }),
        ('Dates and Times', {
            'fields': ('pickup_date', 'return_date', 'actual_pickup_date', 'actual_return_date')
        }),
        ('Pricing', {
            'fields': ('daily_rate', 'total_days', 'subtotal', 'tax_amount', 'insurance_amount', 'additional_fees', 'total_amount')
        }),
        ('Security Deposit', {
            'fields': ('security_deposit', 'deposit_refunded', 'deposit_refund_date')
        }),
        ('Vehicle Condition', {
            'fields': ('pickup_mileage', 'return_mileage', 'pickup_fuel_level', 'return_fuel_level')
        }),
        ('Notes and Staff', {
            'fields': ('pickup_notes', 'return_notes', 'cancellation_reason', 'pickup_staff', 'return_staff')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def is_overdue(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">Overdue ({} days)</span>', obj.days_overdue)
        return 'No'
    is_overdue.short_description = 'Overdue Status'
