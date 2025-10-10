from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import CarBrand, CarCategory, Car
from .serializers import CarBrandSerializer, CarCategorySerializer, CarSerializer, CarListSerializer

class CarBrandListView(generics.ListAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'country', 'created_at']
    ordering = ['name']

class CarCategoryListView(generics.ListAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategorySerializer
    ordering = ['base_price_per_day']

class CarListView(generics.ListAPIView):
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand', 'category', 'transmission', 'fuel_type', 'seats', 'year', 'status']
    search_fields = ['license_plate', 'brand__name', 'model']
    ordering_fields = ['daily_rate', 'year', 'brand__name', 'model']
    ordering = ['brand__name', 'model']
    
    def get_queryset(self):
        queryset = Car.objects.select_related('brand', 'category')
        
        # Filter by availability
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(status='available')
        
        # Price range filter
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price:
            queryset = queryset.filter(daily_rate__gte=min_price)
        if max_price:
            queryset = queryset.filter(daily_rate__lte=max_price)
        
        return queryset

class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.select_related('brand', 'category')
    serializer_class = CarSerializer
    lookup_field = 'pk'

@api_view(['GET'])
def car_availability(request, car_id):
    """Check car availability for specific dates"""
    try:
        car = Car.objects.get(id=car_id)
        pickup_date = request.GET.get('pickup_date')
        return_date = request.GET.get('return_date')
        
        if not pickup_date or not return_date:
            return Response({
                'error': 'pickup_date and return_date parameters are required'
            }, status=400)
        
        # Check if car has any overlapping rentals
        from rentals.models import Rental
        from django.utils.dateparse import parse_datetime
        
        pickup_dt = parse_datetime(pickup_date)
        return_dt = parse_datetime(return_date)
        
        overlapping_rentals = Rental.objects.filter(
            car=car,
            status__in=['confirmed', 'active'],
            pickup_date__lt=return_dt,
            return_date__gt=pickup_dt
        ).exists()
        
        is_available = not overlapping_rentals and car.status == 'available'
        
        return Response({
            'car_id': car_id,
            'available': is_available,
            'car_status': car.status,
            'pickup_date': pickup_date,
            'return_date': return_date,
            'daily_rate': str(car.daily_rate)
        })
        
    except Car.DoesNotExist:
        return Response({'error': 'Car not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# HTML Template Views
def car_list_view(request):
    """HTML view for car listings with filtering"""
    cars = Car.objects.select_related('brand', 'category')
    
    # Apply filters
    category = request.GET.get('category')
    if category:
        cars = cars.filter(category__name=category)
    
    brand = request.GET.get('brand')
    if brand:
        cars = cars.filter(brand_id=brand)
    
    transmission = request.GET.get('transmission')
    if transmission:
        cars = cars.filter(transmission=transmission)
    
    fuel_type = request.GET.get('fuel_type')
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    
    min_price = request.GET.get('min_price')
    if min_price:
        cars = cars.filter(daily_rate__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        cars = cars.filter(daily_rate__lte=max_price)
    
    search = request.GET.get('search')
    if search:
        cars = cars.filter(
            Q(brand__name__icontains=search) |
            Q(model__icontains=search) |
            Q(license_plate__icontains=search)
        )
    
    available_only = request.GET.get('available_only')
    if available_only:
        cars = cars.filter(status='available')
    
    # Pagination
    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    brands = CarBrand.objects.all()
    categories = CarCategory.objects.all()
    
    context = {
        'cars': page_obj,
        'brands': brands,
        'categories': categories,
        'current_filters': {
            'category': category,
            'brand': brand,
            'transmission': transmission,
            'fuel_type': fuel_type,
            'min_price': min_price,
            'max_price': max_price,
            'search': search,
            'available_only': available_only,
        },
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'fuel_choices': Car.FUEL_CHOICES,
    }
    
    return render(request, 'cars/car_list.html', context)

def car_detail_view(request, pk):
    """HTML view for individual car details"""
    car = get_object_or_404(Car.objects.select_related('brand', 'category'), pk=pk)
    
    # Get similar cars
    similar_cars = Car.objects.filter(
        category=car.category,
        status='available'
    ).exclude(pk=car.pk).select_related('brand', 'category')[:4]
    
    context = {
        'car': car,
        'similar_cars': similar_cars,
    }
    
    return render(request, 'cars/car_detail.html', context)

def brand_list_view(request):
    """HTML view for car brands"""
    brands = CarBrand.objects.all().order_by('name')
    
    context = {
        'brands': brands,
    }
    
    return render(request, 'cars/brand_list.html', context)
