from django.http import JsonResponse
from django.shortcuts import render
from cars.models import Car, CarCategory
from customers.models import Customer
from rentals.models import Rental

def home(request):
    """Home page with featured cars and categories"""
    
    # Check if this is an API request
    if request.headers.get('Accept') == 'application/json' or request.path.startswith('/api/'):
        return JsonResponse({
            'message': 'Welcome to Rental Car Management System API',
            'version': '1.0.0',
            'endpoints': {
                'admin': '/admin/',
                'cars': {
                    'list': '/api/cars/',
                    'detail': '/api/cars/{id}/',
                    'availability': '/api/cars/{id}/availability/?pickup_date=2024-01-01T10:00:00Z&return_date=2024-01-05T10:00:00Z',
                    'brands': '/api/cars/brands/',
                    'categories': '/api/cars/categories/',
                },
                'authentication': '/api-auth/',
            },
            'status': 'Running',
            'database': 'SQLite (Development)',
            'note': 'This is a development version using SQLite. PostgreSQL will be used with Docker in production.'
        })
    
    # Render HTML template
    featured_cars = Car.objects.filter(status='available').select_related('brand', 'category')[:6]
    categories = CarCategory.objects.all()[:6]
    
    # Get some stats
    stats = {
        'total_cars': Car.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_rentals': Rental.objects.count(),
        'cities': 25  # Static for now
    }
    
    context = {
        'featured_cars': featured_cars,
        'categories': categories,
        'stats': stats,
    }
    
    return render(request, 'home.html', context)
