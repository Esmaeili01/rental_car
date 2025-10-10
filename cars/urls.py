from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    # HTML Template Views
    path('', views.car_list_view, name='car-list-view'),
    path('<int:pk>/', views.car_detail_view, name='car-detail-view'),
    path('brands/', views.brand_list_view, name='brand-list-view'),
    
    # API Views
    path('api/brands/', views.CarBrandListView.as_view(), name='brand-list'),
    path('api/categories/', views.CarCategoryListView.as_view(), name='category-list'),
    path('api/', views.CarListView.as_view(), name='car-list'),
    path('api/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('api/<int:car_id>/availability/', views.car_availability, name='car-availability'),
]
