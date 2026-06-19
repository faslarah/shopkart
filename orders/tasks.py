from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order Confirmation - OpenMall'
        message = (
            f'Hi {order.first_name},\n\n'
            f'Thank you for shopping at OpenMall!\n'
            f'Your order has been successfully placed and payment is confirmed.\n\n'
            f'Total Amount: ₹{order.total_price}\n'
            f'Shipping Address:\n'
            f'{order.address}, {order.city}, {order.state} - {order.pincode}\n\n'
            f'We will notify you once your order is shipped.\n\n'
            f'Thanks,\nOpenMall Team'
        )
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order.email]
        
        send_mail(subject, message, email_from, recipient_list)
        return f"Order confirmation email sent to {order.email} for order #{order.id}"
    except Order.DoesNotExist:
        return f"Order {order_id} does not exist."
