#!/usr/bin/env python3
"""
Test script to verify image serving works without Werkzeug errors
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_file_serving():
    """Test if file serving works without Werkzeug errors"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test the file serving route
            response = client.get('/uploads/doctors/4eb311e6-2e9a-4ba6-b5cd-5e64ae812a09.webp')
            
            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Content-Length: {response.headers.get('Content-Length')}")
            
            if response.status_code == 200:
                print("✓ File serving works correctly")
                return True
            else:
                print(f"✗ File serving failed with status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"✗ Error testing file serving: {e}")
        return False

def test_file_paths():
    """Test if file paths are correct"""
    upload_folder = 'uploads/doctors'
    test_file = '4eb311e6-2e9a-4ba6-b5cd-5e64ae812a09.webp'
    
    file_path = os.path.join(upload_folder, test_file)
    abs_path = os.path.abspath(file_path)
    
    print(f"Relative path: {file_path}")
    print(f"Absolute path: {abs_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'} bytes")
    
    return os.path.exists(file_path)

def test_werkzeug_compatibility():
    """Test if the response is compatible with Werkzeug"""
    try:
        from app import app
        from flask import send_from_directory
        
        with app.app_context():
            # Test send_from_directory directly
            upload_path = os.path.join(os.getcwd(), 'uploads', 'doctors')
            test_file = '4eb311e6-2e9a-4ba6-b5cd-5e64ae812a09.webp'
            
            if os.path.exists(os.path.join(upload_path, test_file)):
                response = send_from_directory(upload_path, test_file, as_attachment=False)
                print(f"✓ send_from_directory works: {type(response)}")
                return True
            else:
                print("✗ Test file not found")
                return False
                
    except Exception as e:
        print(f"✗ Error testing Werkzeug compatibility: {e}")
        return False

if __name__ == "__main__":
    print("Testing Image Serving (Werkzeug Fix)...")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing file paths...")
    success &= test_file_paths()
    
    print("\n2. Testing Werkzeug compatibility...")
    success &= test_werkzeug_compatibility()
    
    print("\n3. Testing file serving...")
    success &= test_file_serving()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All image serving tests passed!")
        print("Images should now display correctly without Werkzeug errors.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
