from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, PaymentMethod

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'customer', 'rental', 'payment_type', 'amount', 'status', 'payment_date', 'payment_status']
    list_filter = ['status', 'payment_type', 'payment_method', 'payment_date']
    search_fields = ['payment_id', 'customer__user__username', 'customer__user__email', 'rental__rental_id', 'transaction_id']
    list_editable = ['status']
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'rental', 'customer', 'payment_type', 'status')
        }),
        ('Payment Details', {
            'fields': ('amount', 'currency', 'payment_method', 'card_last_four', 'description')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'external_payment_id', 'payment_date', 'processed_date')
        }),
        ('Additional Information', {
            'fields': ('failure_reason', 'processed_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def payment_status(self, obj):
        if obj.status == 'completed':
            return format_html('<span style="color: green; font-weight: bold;">✓ {}</span>', obj.get_status_display())
        elif obj.status == 'failed':
            return format_html('<span style="color: red; font-weight: bold;">✗ {}</span>', obj.get_status_display())
        elif obj.status == 'pending':
            return format_html('<span style="color: orange; font-weight: bold;">⏳ {}</span>', obj.get_status_display())
        else:
            return obj.get_status_display()
    payment_status.short_description = 'Status'
    payment_status.admin_order_field = 'status'

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['customer', 'card_type', 'last_four_digits', 'is_default', 'is_active', 'created_at']
    list_filter = ['card_type', 'is_default', 'is_active', 'created_at']
    search_fields = ['customer__user__username', 'customer__user__email', 'last_four_digits', 'cardholder_name']
    list_editable = ['is_default', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer', {
            'fields': ('customer',)
        }),
        ('Card Information', {
            'fields': ('card_type', 'last_four_digits', 'expiry_month', 'expiry_year', 'cardholder_name')
        }),
        ('Payment Gateway', {
            'fields': ('payment_token', 'gateway_customer_id')
        }),
        ('Status', {
            'fields': ('is_default', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
