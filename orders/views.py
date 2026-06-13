from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem


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
            paid        = True,
        )
        for item in cart:
            OrderItem.objects.create(
                order    = order,
                product  = item['product'],
                price    = item['price'],
                quantity = item['quantity'],
            )
        cart.clear()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})