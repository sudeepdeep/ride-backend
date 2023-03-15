from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
import smtplib

def send_otp_email(email):
    subject = 'OTP'
    otp = random.randint(1000, 9999)
    message = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)
    try:
        user_obj = User.objects.get(username=email)
        user_obj.otp = otp
        user_obj.save()
    except User.DoesNotExist:
        user_obj = None
    