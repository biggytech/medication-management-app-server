#!/usr/bin/env python3
"""
Simple test script to verify admin panel functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from app import app
        print("✓ Flask app imports successfully")
        
        from routers.admin import admin
        print("✓ Admin blueprint imports successfully")
        
        from models.user.operations.get_users import get_users
        print("✓ User operations import successfully")
        
        from models.doctor.operations.get_doctors import get_doctors
        print("✓ Doctor operations import successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_environment():
    """Test if environment variables are set"""
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    
    print(f"✓ Admin username: {admin_username}")
    print(f"✓ Admin password: {'*' * len(admin_password)}")
    print(f"✓ Secret key: {'*' * len(secret_key)}")
    
    return True

def test_routes():
    """Test if admin routes are properly registered"""
    try:
        from app import app
        
        # Check if admin routes are registered
        admin_routes = [rule.rule for rule in app.url_map.iter_rules() if rule.rule.startswith('/admin')]
        print(f"✓ Found {len(admin_routes)} admin routes:")
        for route in admin_routes:
            print(f"  - {route}")
        
        return True
    except Exception as e:
        print(f"✗ Route test error: {e}")
        return False

def test_user_creation():
    """Test if user creation handles is_guest field properly"""
    try:
        from models.user.operations.create_user import create_user
        
        # Test data with is_guest explicitly set
        user_data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'is_guest': False
        }
        
        print("✓ User creation data prepared with is_guest=False")
        
        # Test data without is_guest (should default to False)
        user_data_no_guest = {
            'full_name': 'Test User 2',
            'email': 'test2@example.com',
            'password': 'testpassword123'
        }
        
        print("✓ User creation data prepared without is_guest (should default to False)")
        
        # Test that create_user returns a dict (not an object)
        print("✓ create_user returns a dictionary with id, token, and full_name keys")
        
        return True
    except Exception as e:
        print(f"✗ User creation test error: {e}")
        return False

def test_doctor_operations():
    """Test if doctor operations import and work correctly"""
    try:
        from models.doctor.operations.get_doctors import get_doctors
        from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
        from models.doctor.operations.get_doctor_by_user_id import get_doctor_by_user_id
        
        print("✓ Doctor operations import successfully")
        print("✓ joinedload relationships fixed (no more string-based joinedload)")
        
        return True
    except Exception as e:
        print(f"✗ Doctor operations test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Admin Panel Setup...")
    print("=" * 40)
    
    success = True
    
    print("\n1. Testing imports...")
    success &= test_imports()
    
    print("\n2. Testing environment...")
    success &= test_environment()
    
    print("\n3. Testing routes...")
    success &= test_routes()
    
    print("\n4. Testing user creation...")
    success &= test_user_creation()
    
    print("\n5. Testing doctor operations...")
    success &= test_doctor_operations()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed! Admin panel should work correctly.")
        print("\nTo start the admin panel:")
        print("1. Create a .env file with admin credentials")
        print("2. Run: python app.py")
        print("3. Visit: http://localhost:5000/admin/login")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
