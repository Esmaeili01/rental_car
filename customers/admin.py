from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'license_number', 'is_verified', 'is_blacklisted', 'created_at']
    list_filter = ['is_verified', 'is_blacklisted', 'country', 'license_state', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'license_number', 'phone_number']
    list_editable = ['is_verified', 'is_blacklisted']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Driver\'s License', {
            'fields': ('license_number', 'license_expiry', 'license_state')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Account Status', {
            'fields': ('is_verified', 'verification_date', 'is_blacklisted', 'blacklist_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
