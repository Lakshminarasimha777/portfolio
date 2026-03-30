from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Lead

# Home Page
def home(request):
    return render(request, 'home.html')


# Register (Lead User)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken.')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'register.html')


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard' if user.is_staff else 'user_dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# Logout
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')


# User Dashboard
@login_required(login_url='login')
def user_dashboard(request):
    query = request.GET.get('q')

    if query:
        leads = Lead.objects.filter(user=request.user, name__icontains=query)
    else:
        leads = Lead.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()

        if not name or not email:
            messages.error(request, 'Name and email are required to add a lead.')
            return redirect('user_dashboard')

        Lead.objects.create(user=request.user, name=name, email=email)
        messages.success(request, 'Lead added successfully.')
        return redirect('user_dashboard')

    return render(request, 'user_dashboard.html', {'leads': leads})

# Admin Dashboard
@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    query = request.GET.get('q')  # get search text

    if query:
        leads = Lead.objects.filter(name__icontains=query) | Lead.objects.filter(email__icontains=query)
    else:
        leads = Lead.objects.all()

    return render(request, 'admin_dashboard.html', {'leads': leads})

# Delete Lead
@login_required(login_url='login')
def delete_lead(request, id):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    lead = get_object_or_404(Lead, id=id)
    lead.delete()
    messages.success(request, 'Lead deleted successfully.')
    return redirect('admin_dashboard')


