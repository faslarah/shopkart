from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import stripe
from cart.cart import Cart
from .models import Order, OrderItem
from accounts.loyalty import award_points

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:home')

    if request.method == 'POST':
        # Handle points redemption
        points_to_use = int(request.POST.get('use_points', 0) or 0)
        discount = 0
        if points_to_use >= 100:
            from accounts.loyalty import redeem_points
            discount = redeem_points(request.user, points_to_use)

        total = max(cart.get_total_price() - discount, 0)

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
            total_price = total,
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
            earned = award_points(request.user, total)
            cart.clear()
            messages.success(request, f'Order #{order.id} placed! You earned {earned} loyalty points.')
            return redirect('orders:order_detail', order_id=order.id)

        elif payment_method == 'stripe':
            return redirect('orders:stripe_payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def stripe_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.name,
                    'description': item.product.brand or 'OpenMall Product',
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
        success_url=request.build_absolute_uri(f'/orders/success/{order.id}/'),
        cancel_url=request.build_absolute_uri(f'/orders/cancel/{order.id}/'),
        metadata={'order_id': order.id},
    )

    return redirect(session.url, permanent=False)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.save()
    earned = award_points(request.user, order.total_price)
    cart = Cart(request)
    cart.clear()
    messages.success(request, f'Payment successful! Order #{order.id} confirmed. You earned {earned} loyalty points.')
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