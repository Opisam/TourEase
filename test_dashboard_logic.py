import os
import django
from django.test import RequestFactory
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourease.settings')
django.setup()

from tours.views import provider_dashboard
from accounts.models import User
from tours.models import TourPackage

try:
    # Get the provider user
    user = User.objects.get(username='opisam')
    
    # Create a request factory
    factory = RequestFactory()
    request = factory.get(reverse('provider_dashboard'))
    request.user = user
    
    # Call the view (as a function)
    # Note: provider_dashboard is a decorated function (at line 122)
    # We call it directly to check the context
    # Usually we wrap the test in TestCase to handle DB state
    
    from django.test import TestCase
    class DashboardTest(TestCase):
        def test_dashboard_context(self):
            # We assume the DB has the tours already from the user's manual work
            # But here we are in a fresh test DB if using TestCase
            pass
            
    # Instead, let's just count them in simple python to verify logic
    tours = TourPackage.objects.filter(company=user)
    approved_tours_count = tours.filter(is_approved=True).count()
    total_bookings_count = tours.aggregate(count=django.db.models.Count('bookings'))['count'] # wait, that's not right
    
    print(f"User: {user.username}")
    print(f"Total Tours: {tours.count()}")
    print(f"Approved Tours Count: {approved_tours_count}")
    
except Exception as e:
    print(f"ERROR: {e}")
