#!/usr/bin/env python
"""
Test script for Celery tasks
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
django.setup()

from apps.multiparser.tasks import download_and_save_file, update_parsed_data_periodic, cleanup_old_files

def test_celery_tasks():
    """Test Celery tasks"""
    print("Testing Celery tasks...")
    
    # Test periodic update task
    print("1. Testing periodic update task...")
    try:
        result = update_parsed_data_periodic.delay()
        print(f"   Task submitted: {result.id}")
        print(f"   Task status: {result.status}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test cleanup task
    print("2. Testing cleanup task...")
    try:
        result = cleanup_old_files.delay()
        print(f"   Task submitted: {result.id}")
        print(f"   Task status: {result.status}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nCelery test completed!")
    print("Check the Celery worker output for task execution details.")

if __name__ == "__main__":
    test_celery_tasks()
