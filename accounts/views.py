from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Profile
from orders.models import Order


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created! Welcome to ShopKart.')
            return redirect('store:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user     = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('store:home')


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile_obj)

    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders, 'profile': profile_obj})