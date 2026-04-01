import os
import django
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourease.settings')
django.setup()

try:
    print("Attempting to send a test email to dopio8081@gmail.com...")
    send_mail(
        'SMTP Connection Test',
        'This is a test email to verify your SMTP settings in TourEase.',
        'dopio8081@gmail.com',
        ['dopio8081@gmail.com'],
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"FAILED to send email: {type(e).__name__}: {e}")
