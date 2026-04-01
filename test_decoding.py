import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourease.settings')
django.setup()

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.forms import SetPasswordForm
from accounts.models import User

uid = 'NA'
try:
    decoded_uid = force_str(urlsafe_base64_decode(uid))
    print(f"Decoded UID: {decoded_uid}")
    user = User.objects.get(pk=decoded_uid)
    print(f"User found: {user.username} (ID: {user.pk})")
    
    form = SetPasswordForm(user=user)
    print("Form fields:")
    for field in form:
        print(f" - {field.name}: {field.label}")
except Exception as e:
    print(f"ERROR: {e}")
