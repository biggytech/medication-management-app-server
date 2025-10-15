#!/usr/bin/env python3
"""
Test script to verify file serving functionality
"""

import os
import requests
from app import app

def test_file_serving():
    """Test if uploaded files can be served correctly"""
    with app.test_client() as client:
        # Test the file serving route
        response = client.get('/uploads/doctors/4eb311e6-2e9a-4ba6-b5cd-5e64ae812a09.webp')
        
        if response.status_code == 200:
            print("✓ File serving works correctly")
            print(f"✓ Content-Type: {response.headers.get('Content-Type')}")
            print(f"✓ Content-Length: {response.headers.get('Content-Length')}")
            return True
        else:
            print(f"✗ File serving failed with status: {response.status_code}")
            return False

def test_file_paths():
    """Test if file paths are correct"""
    upload_folder = 'uploads/doctors'
    test_file = '4eb311e6-2e9a-4ba6-b5cd-5e64ae812a09.webp'
    
    file_path = os.path.join(upload_folder, test_file)
    
    if os.path.exists(file_path):
        print(f"✓ File exists at: {file_path}")
        return True
    else:
        print(f"✗ File not found at: {file_path}")
        return False

if __name__ == "__main__":
    print("Testing File Serving...")
    print("=" * 40)
    
    success = True
    
    print("\n1. Testing file existence...")
    success &= test_file_paths()
    
    print("\n2. Testing file serving...")
    success &= test_file_serving()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All file serving tests passed!")
        print("\nFile serving should work correctly now.")
        print("Photo URLs should be accessible at: /uploads/doctors/<filename>")
    else:
        print("✗ Some tests failed. Please check the errors above.")
