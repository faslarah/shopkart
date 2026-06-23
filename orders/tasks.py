from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order

def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order Confirmation - OpenMall'
        
        # Render HTML content
        html_content = render_to_string('emails/order_confirmation.html', {'order': order})
        # Create a plain text fallback
        text_content = strip_tags(html_content)
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order.email]
        
        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        return f"Order confirmation email sent to {order.email} for order #{order.id}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
