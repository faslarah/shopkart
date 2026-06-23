from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Profile, LoyaltySettings
from orders.models import Order


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created! Welcome to OpenMall.')
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
    orders         = Order.objects.filter(user=request.user)
    ls             = LoyaltySettings.get_settings()

    if request.method == 'POST':
        profile_obj.phone   = request.POST.get('phone', '')
        profile_obj.address = request.POST.get('address', '')
        profile_obj.city    = request.POST.get('city', '')
        profile_obj.state   = request.POST.get('state', '')
        profile_obj.pincode = request.POST.get('pincode', '')
        if 'avatar' in request.FILES:
            profile_obj.avatar = request.FILES['avatar']
        profile_obj.save()
        messages.success(request, 'Profile updated.')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'profile': profile_obj,
        'orders':  orders,
        'ls':      ls,
    })


@login_required
def points_page(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/points.html', {
        'profile': profile_obj,
    })


@login_required
def notifications(request):
    return render(request, 'accounts/notifications.html', {})


@staff_member_required
def loyalty_settings(request):
    settings = LoyaltySettings.get_settings()

    if request.method == 'POST':
        settings.spend_amount      = int(request.POST.get('spend_amount', 1))
        settings.points_per_spend  = int(request.POST.get('points_per_spend', 1))
        settings.points_to_rupee   = int(request.POST.get('points_to_rupee', 100))
        settings.rupee_per_redeem  = int(request.POST.get('rupee_per_redeem', 10))
        settings.min_redeem_points = int(request.POST.get('min_redeem_points', 500))
        settings.is_active         = 'is_active' in request.POST
        settings.save()
        messages.success(request, 'Loyalty settings updated successfully!')
        return redirect('accounts:loyalty_settings')

    return render(request, 'accounts/loyalty_settings.html', {
        'settings': settings,
    })