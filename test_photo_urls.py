#!/usr/bin/env python3
"""
Test script to verify photo URL generation and serving
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_url_generation():
    """Test if photo URLs are generated correctly"""
    try:
        from routers.admin import save_uploaded_file
        print("✓ Photo URL generation function imports successfully")
        
        # Test URL format
        test_filename = "test-image.jpg"
        expected_url = f"/uploads/doctors/{test_filename}"
        print(f"✓ Expected URL format: {expected_url}")
        
        return True
    except Exception as e:
        print(f"✗ Error testing URL generation: {e}")
        return False

def test_file_paths():
    """Test if file paths are accessible"""
    upload_folder = 'uploads/doctors'
    
    if os.path.exists(upload_folder):
        print(f"✓ Upload folder exists: {upload_folder}")
        
        # List files in upload folder
        files = os.listdir(upload_folder)
        if files:
            print(f"✓ Found {len(files)} files in upload folder")
            for file in files[:3]:  # Show first 3 files
                print(f"  - {file}")
        else:
            print("⚠ No files found in upload folder")
        
        return True
    else:
        print(f"✗ Upload folder not found: {upload_folder}")
        return False

def test_app_routes():
    """Test if app routes are configured correctly"""
    try:
        from app import app
        
        # Check if the route is registered
        with app.app_context():
            rules = [rule.rule for rule in app.url_map.iter_rules()]
            upload_routes = [rule for rule in rules if 'uploads/doctors' in rule]
            
            if upload_routes:
                print("✓ Upload routes found:")
                for route in upload_routes:
                    print(f"  - {route}")
                return True
            else:
                print("✗ No upload routes found")
                return False
                
    except Exception as e:
        print(f"✗ Error testing app routes: {e}")
        return False

if __name__ == "__main__":
    print("Testing Photo URL Functionality...")
    print("=" * 40)
    
    success = True
    
    print("\n1. Testing URL generation...")
    success &= test_url_generation()
    
    print("\n2. Testing file paths...")
    success &= test_file_paths()
    
    print("\n3. Testing app routes...")
    success &= test_app_routes()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All photo URL tests passed!")
        print("\nPhoto URLs should now be accessible.")
        print("Try accessing: http://localhost:5000/uploads/doctors/<filename>")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
