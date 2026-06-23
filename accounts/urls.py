from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register,  name='register'),
    path('login/',    views.user_login, name='login'),
    path('logout/',   views.user_logout,name='logout'),
    path('profile/',  views.profile,    name='profile'),
    path('points/',    views.points_page, name='points'),
    path('loyalty-settings/', views.loyalty_settings,  name='loyalty_settings'),
]