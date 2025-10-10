from django.core.management.base import BaseCommand
from cars.models import CarBrand, CarCategory, Car
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample data for the rental car system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create Car Brands
        brands_data = [
            {'name': 'Toyota', 'country': 'Japan'},
            {'name': 'Honda', 'country': 'Japan'},
            {'name': 'Ford', 'country': 'USA'},
            {'name': 'BMW', 'country': 'Germany'},
            {'name': 'Audi', 'country': 'Germany'},
            {'name': 'Mercedes-Benz', 'country': 'Germany'},
            {'name': 'Hyundai', 'country': 'South Korea'},
            {'name': 'Nissan', 'country': 'Japan'},
        ]

        for brand_data in brands_data:
            brand, created = CarBrand.objects.get_or_create(**brand_data)
            if created:
                self.stdout.write(f'Created brand: {brand.name}')

        # Create Car Categories
        categories_data = [
            {'name': 'economy', 'base_price_per_day': Decimal('25.00'), 'description': 'Affordable and fuel-efficient vehicles'},
            {'name': 'compact', 'base_price_per_day': Decimal('35.00'), 'description': 'Small to medium sized cars'},
            {'name': 'mid_size', 'base_price_per_day': Decimal('45.00'), 'description': 'Comfortable medium-sized vehicles'},
            {'name': 'full_size', 'base_price_per_day': Decimal('55.00'), 'description': 'Large comfortable sedans'},
            {'name': 'premium', 'base_price_per_day': Decimal('75.00'), 'description': 'High-end vehicles with premium features'},
            {'name': 'luxury', 'base_price_per_day': Decimal('120.00'), 'description': 'Top-tier luxury vehicles'},
            {'name': 'suv', 'base_price_per_day': Decimal('65.00'), 'description': 'Sport Utility Vehicles'},
        ]

        for category_data in categories_data:
            category, created = CarCategory.objects.get_or_create(**category_data)
            if created:
                self.stdout.write(f'Created category: {category.get_name_display()}')

        # Create Sample Cars
        toyota = CarBrand.objects.get(name='Toyota')
        honda = CarBrand.objects.get(name='Honda')
        ford = CarBrand.objects.get(name='Ford')
        bmw = CarBrand.objects.get(name='BMW')
        audi = CarBrand.objects.get(name='Audi')
        mercedes = CarBrand.objects.get(name='Mercedes-Benz')

        economy = CarCategory.objects.get(name='economy')
        compact = CarCategory.objects.get(name='compact')
        mid_size = CarCategory.objects.get(name='mid_size')
        premium = CarCategory.objects.get(name='premium')
        luxury = CarCategory.objects.get(name='luxury')
        suv = CarCategory.objects.get(name='suv')

        cars_data = [
            # Economy Cars
            {
                'license_plate': 'ABC123', 'brand': toyota, 'model': 'Corolla', 'year': 2023,
                'category': economy, 'engine_capacity': Decimal('1.8'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('28.00'),
                'mileage': 15000, 'status': 'available'
            },
            {
                'license_plate': 'DEF456', 'brand': honda, 'model': 'Civic', 'year': 2022,
                'category': compact, 'engine_capacity': Decimal('2.0'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('38.00'),
                'mileage': 22000, 'status': 'available'
            },
            {
                'license_plate': 'GHI789', 'brand': toyota, 'model': 'Camry', 'year': 2023,
                'category': mid_size, 'engine_capacity': Decimal('2.5'), 'transmission': 'automatic',
                'fuel_type': 'hybrid', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('48.00'),
                'mileage': 8000, 'status': 'available'
            },
            # Premium Cars
            {
                'license_plate': 'JKL012', 'brand': bmw, 'model': '3 Series', 'year': 2024,
                'category': premium, 'engine_capacity': Decimal('2.0'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('78.00'),
                'mileage': 5000, 'status': 'available'
            },
            {
                'license_plate': 'MNO345', 'brand': audi, 'model': 'A4', 'year': 2023,
                'category': premium, 'engine_capacity': Decimal('2.0'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('82.00'),
                'mileage': 12000, 'status': 'available'
            },
            # Luxury Cars
            {
                'license_plate': 'PQR678', 'brand': mercedes, 'model': 'E-Class', 'year': 2024,
                'category': luxury, 'engine_capacity': Decimal('3.0'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('125.00'),
                'mileage': 3000, 'status': 'available'
            },
            # SUVs
            {
                'license_plate': 'STU901', 'brand': toyota, 'model': 'RAV4', 'year': 2023,
                'category': suv, 'engine_capacity': Decimal('2.5'), 'transmission': 'automatic',
                'fuel_type': 'hybrid', 'seats': 5, 'doors': 5, 'daily_rate': Decimal('68.00'),
                'mileage': 18000, 'status': 'available'
            },
            {
                'license_plate': 'VWX234', 'brand': ford, 'model': 'Explorer', 'year': 2022,
                'category': suv, 'engine_capacity': Decimal('3.3'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 7, 'doors': 5, 'daily_rate': Decimal('72.00'),
                'mileage': 25000, 'status': 'available'
            },
            # Some cars under maintenance or rented
            {
                'license_plate': 'YZA567', 'brand': honda, 'model': 'Accord', 'year': 2023,
                'category': mid_size, 'engine_capacity': Decimal('2.0'), 'transmission': 'automatic',
                'fuel_type': 'hybrid', 'seats': 5, 'doors': 4, 'daily_rate': Decimal('52.00'),
                'mileage': 11000, 'status': 'rented'
            },
            {
                'license_plate': 'BCD890', 'brand': bmw, 'model': 'X5', 'year': 2023,
                'category': luxury, 'engine_capacity': Decimal('3.0'), 'transmission': 'automatic',
                'fuel_type': 'petrol', 'seats': 7, 'doors': 5, 'daily_rate': Decimal('135.00'),
                'mileage': 7500, 'status': 'maintenance'
            },
        ]

        for car_data in cars_data:
            car, created = Car.objects.get_or_create(
                license_plate=car_data['license_plate'],
                defaults=car_data
            )
            if created:
                self.stdout.write(f'Created car: {car.full_name} ({car.license_plate})')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created sample data!')
        )
        
        # Show summary
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'- Car Brands: {CarBrand.objects.count()}')
        self.stdout.write(f'- Car Categories: {CarCategory.objects.count()}')
        self.stdout.write(f'- Cars: {Car.objects.count()}')
        self.stdout.write(f'- Available Cars: {Car.objects.filter(status="available").count()}')
        self.stdout.write(f'- Rented Cars: {Car.objects.filter(status="rented").count()}')
        self.stdout.write(f'- Cars in Maintenance: {Car.objects.filter(status="maintenance").count()}')