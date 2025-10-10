from rest_framework import serializers
from .models import CarBrand, CarCategory, Car

class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = '__all__'

class CarCategorySerializer(serializers.ModelSerializer):
    car_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CarCategory
        fields = '__all__'
    
    def get_car_count(self, obj):
        return obj.cars.filter(status='available').count()

class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    full_name = serializers.CharField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Car
        fields = '__all__'

class CarListSerializer(serializers.ModelSerializer):
    """Simplified serializer for car listings"""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Car
        fields = [
            'id', 'license_plate', 'brand_name', 'model', 'year', 
            'category_name', 'daily_rate', 'status', 'image', 
            'full_name', 'seats', 'doors', 'fuel_type', 'transmission'
        ]