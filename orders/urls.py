from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/',              views.checkout,         name='checkout'),
    path('stripe/<int:order_id>/', views.stripe_payment,   name='stripe_payment'),
    path('cod/<int:order_id>/',    views.cod_confirm,      name='cod_confirm'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('cancel/<int:order_id>/', views.payment_cancel,   name='payment_cancel'),
    path('my-orders/',             views.order_list,       name='order_list'),
    path('<int:order_id>/',        views.order_detail,     name='order_detail'),
]