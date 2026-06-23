from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import stripe
from cart.cart import Cart
from .models import Order, OrderItem
from .tasks import send_order_confirmation_email
from accounts.models import LoyaltySettings, Profile

stripe.api_key = settings.STRIPE_SECRET_KEY


def award_purchase_points(user, order):
    ls = LoyaltySettings.get_settings()
    if not ls.is_active:
        return 0
    profile, _ = Profile.objects.get_or_create(user=user)
    points_earned = int(float(order.total_price) / ls.spend_amount) * ls.points_per_spend
    profile.points += points_earned
    profile.save()
    return points_earned


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:home')

    ls         = LoyaltySettings.get_settings()
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        redeem_points   = int(request.POST.get('redeem_points', 0))
        points_discount = 0

        if ls.is_active and redeem_points > 0:
            if redeem_points < ls.min_redeem_points:
                messages.error(request, f'Minimum {ls.min_redeem_points} points required.')
                return redirect('orders:checkout')
            if redeem_points > profile.points:
                messages.error(request, 'Insufficient points.')
                return redirect('orders:checkout')
            points_discount = (redeem_points / ls.points_to_rupee) * ls.rupee_per_redeem
            points_discount = min(points_discount, float(cart.get_total_price()))

        total = float(cart.get_total_price()) - points_discount

        order = Order.objects.create(
            user            = request.user,
            first_name      = request.POST['first_name'],
            last_name       = request.POST['last_name'],
            email           = request.POST['email'],
            phone           = request.POST['phone'],
            address         = request.POST['address'],
            city            = request.POST['city'],
            state           = request.POST['state'],
            pincode         = request.POST['pincode'],
            total_price     = max(total, 0),
            points_redeemed = redeem_points,
            paid            = False,
        )
        for item in cart:
            OrderItem.objects.create(
                order    = order,
                product  = item['product'],
                price    = item['price'],
                quantity = item['quantity'],
            )

        if ls.is_active and redeem_points > 0:
            profile.points          -= redeem_points
            profile.points_redeemed += redeem_points
            profile.save()

        # Route based on payment method chosen in checkout form
        payment_method = request.POST.get('payment', 'cod')
        if payment_method == 'stripe':
            return redirect('orders:stripe_payment', order_id=order.id)
        else:
            return redirect('orders:cod_confirm', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart':    cart,
        'profile': profile,
        'ls':      ls,
    })


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
                'unit_amount': int(float(item.price) * 100),
            },
            'quantity': item.quantity,
        })

    session_kwargs = {
        'payment_method_types': ['card'],
        'line_items':           line_items,
        'mode':                 'payment',
        'customer_email':       order.email,
        'success_url':          request.build_absolute_uri(f'/orders/success/{order.id}/'),
        'cancel_url':           request.build_absolute_uri(f'/orders/cancel/{order.id}/'),
        'metadata':             {'order_id': order.id},
    }

    # Apply loyalty discount if points were redeemed
    subtotal = sum(float(item.price) * item.quantity for item in order.items.all())
    discount = subtotal - float(order.total_price)
    if discount > 0:
        coupon = stripe.Coupon.create(
            amount_off = int(discount * 100),
            currency   = 'inr',
            duration   = 'once',
            name       = 'Loyalty Points Discount'
        )
        session_kwargs['discounts'] = [{'coupon': coupon.id}]

    session = stripe.checkout.Session.create(**session_kwargs)
    return redirect(session.url, permanent=False)


@login_required
def cod_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.status = 'processing'
    order.save()
    cart = Cart(request)
    cart.clear()
    earned = award_purchase_points(request.user, order)
    send_order_confirmation_email(order.id)
    messages.success(request, f'Order #{order.id} placed! You earned {earned} loyalty points.')
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.status = 'processing'
    order.save()
    cart = Cart(request)
    cart.clear()
    earned = award_purchase_points(request.user, order)
    send_order_confirmation_email(order.id)
    messages.success(request, f'Payment successful! Order #{order.id} confirmed. You earned {earned} loyalty points.')
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.points_redeemed > 0:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.points          += order.points_redeemed
        profile.points_redeemed -= order.points_redeemed
        profile.save()

    order.delete()
    messages.error(request, 'Payment cancelled. Loyalty points have been refunded.')
    return redirect('cart:cart_detail')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})