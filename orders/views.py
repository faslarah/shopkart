from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from cart.cart import Cart
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:home')

    if request.method == 'POST':
        order = Order.objects.create(
            user        = request.user,
            first_name  = request.POST['first_name'],
            last_name   = request.POST['last_name'],
            email       = request.POST['email'],
            phone       = request.POST['phone'],
            address     = request.POST['address'],
            city        = request.POST['city'],
            state       = request.POST['state'],
            pincode     = request.POST['pincode'],
            total_price = cart.get_total_price(),
            paid        = False,
        )
        for item in cart:
            OrderItem.objects.create(
                order    = order,
                product  = item['product'],
                price    = item['price'],
                quantity = item['quantity'],
            )

        payment_method = request.POST.get('payment')

        if payment_method == 'cod':
            order.paid = True
            order.save()
            cart.clear()
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('orders:order_detail', order_id=order.id)

        elif payment_method == 'stripe':
            return redirect('orders:stripe_payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def stripe_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Create Stripe Checkout Session (hosted page like in your photo)
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.name,
                    'description': item.product.brand or 'ShopKart Product',
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        customer_email=order.email,
        success_url=request.build_absolute_uri(
            f'/orders/success/{order.id}/'
        ),
        cancel_url=request.build_absolute_uri(
            f'/orders/cancel/{order.id}/'
        ),
        metadata={'order_id': order.id},
    )

    return redirect(session.url, permanent=False)

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.save()

    cart = Cart(request)
    cart.clear()

    messages.success(request, f'Payment successful! Order #{order.id} confirmed.')
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.error(request, 'Payment cancelled. Your order was not placed.')
    return redirect('cart:cart_detail')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
