from django.shortcuts import render, get_object_or_404
from .models import Car
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .forms import SignUpForm , CarForm
from .models import User, Login , Car


def home_view(request):
    cars = Car.objects.filter(status='available')
    return render(request, 'main/home.html', {'cars': cars})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()

            # Log the signup
            Login.objects.create(user=user, is_signup=True)

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user (email-based authentication)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Log the login event
            Login.objects.create(user=user, is_signup=False)

            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('home')  # or wherever your app’s main page is
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'main/login.html')
    
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    return render(request, 'main/profile/profile.html')

def rents_history_view(request):
    # Add logic later to fetch user's rent history
    return render(request, 'main/profile/rents_history.html')

def my_cars_view(request):
    # For owners
    my_cars = Car.objects.filter(owner_id=request.user)
    return render(request, 'main/profile/my_cars.html', {'my_cars': my_cars})

def reports_view(request):
    # For admins
    return render(request, 'main/profile/reports.html')


def suspend_view(request):
    # For admins
    return render(request, 'main/profile/suspend.html')

def manage_admins_view(request):
    # For superadmins
    admins = User.objects.filter(role='admin')
    return render(request, 'main/profile/manage_admins.html', {'admins': admins})

def car_detail_view(request, car_id):
    car = Car.objects.get(pk=car_id)
    return render(request, 'main/car_detail.html', {'car': car})

def add_car_view(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('home')
    else:
        form = CarForm()
    return render(request, 'main/add_car.html', {'form': form})


def search_view(request):
    query = request.GET.get('q')
    cars = Car.objects.filter(brand__icontains=query) if query else []
    return render(request, 'main/search.html', {'cars': cars, 'query': query})

def rents_view(request):
    return render(request, 'main/rents.html')

