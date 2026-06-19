from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, user_name):
    subject = 'Welcome to OpenMall!'
    message = f'Hi {user_name},\n\nThank you for registering at OpenMall.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list)
    return f"Email sent successfully to {user_email}"