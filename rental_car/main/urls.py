from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),

    path('search/', views.search_view, name='search'),
    path('rents/', views.rents_view, name='rents'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # account section
    path('profile/', views.profile_view, name='profile'),
    path('rents_history/', views.rents_history_view, name='rents_history'),
    path('my_cars/', views.my_cars_view, name='my_cars'),
    path('reports/', views.reports_view, name='reports'),
    path('suspend/', views.suspend_view, name='suspend'),
    path('manage_admins/', views.manage_admins_view, name='manage_admins'),

    # Cars
    path('car/<int:car_id>/rent/', views.rent_car_view, name='rent_car'),
    path('car/<int:car_id>/', views.car_view, name='car'),
    path('add_car/', views.add_car_view, name='add_car'),
]