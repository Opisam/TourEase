import os
import django
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourease.settings')
django.setup()

from accounts.models import User

try:
    user = User.objects.get(email='dopio8081@gmail.com')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    print(f"User PK: {user.pk}")
    print(f"Encoded UID: {uid}")
    print(f"Generated Token: {token}")
    
    url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    print(f"Resolved URL: {url}")
except Exception as e:
    print(f"ERROR: {e}")
