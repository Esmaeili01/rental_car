from django.contrib import admin
from .models import CarBrand, CarCategory, Car

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'country']
    ordering = ['name']

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price_per_day', 'get_car_count']
    list_filter = ['name']
    ordering = ['base_price_per_day']
    
    def get_car_count(self, obj):
        return obj.cars.count()
    get_car_count.short_description = 'Number of Cars'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'brand', 'model', 'year', 'category', 'status', 'daily_rate']
    list_filter = ['status', 'brand', 'category', 'transmission', 'fuel_type', 'year']
    search_fields = ['license_plate', 'brand__name', 'model']
    list_editable = ['status', 'daily_rate']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['brand__name', 'model', 'year']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('license_plate', 'brand', 'model', 'year', 'category')
        }),
        ('Technical Specifications', {
            'fields': ('engine_capacity', 'transmission', 'fuel_type', 'seats', 'doors')
        }),
        ('Rental Information', {
            'fields': ('daily_rate', 'mileage', 'status')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
