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

    # Profile section
    path('profile/', views.profile_view, name='profile'),
    path('profile/rents_history/', views.rents_history_view, name='rent_history'),
    path('profile/my_cars/', views.my_cars_view, name='my_cars'),
    path('profile/reports/', views.reports_view, name='reports'),
    path('profile/suspend/', views.suspend_view, name='suspend'),
    path('profile/manage_admins/', views.manage_admins_view, name='manage_admins'),

    # Cars
    path('car/<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('add_car/', views.add_car_view, name='add_car'),
]