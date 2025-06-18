#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from auths.models import CustomUser
from helpers.local_chat_api import register_user_to_chat

print("Testing local chat registration...")

# Test local chat registration
try:
    result = register_user_to_chat("+77123456789", "testpass123")
    print(f"✅ Local chat registration result: {result}")
except Exception as e:
    print(f"❌ Local chat registration failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting user creation...")

# Test user creation manually
try:
    # Delete existing user first
    CustomUser.objects.filter(phone="+77123456789").delete()
    
    # Test user creation step by step - correct parameters for create_user
    print("Creating user...")
    user = CustomUser.objects.create_user(
        phone='+77123456789',
        password='testpass123',  # Required parameter
        email='test@example.com',
        first_name='Test',
        last_name='User',
        middle_name='Middle',
        birthdate='1990-01-01',
        iin='123456789012',
        role='CITIZEN'  # Required parameter
    )
    print(f"✅ User created: {user.id}")
    
    print("User is active:", user.is_active)
    print("User phone:", user.phone)
    print("User role:", user.role)
    
except Exception as e:
    print(f"❌ User creation failed: {e}")
    import traceback
    traceback.print_exc()

print("\nDone.") 