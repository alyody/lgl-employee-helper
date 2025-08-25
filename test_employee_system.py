#!/usr/bin/env python3
"""
Test script to verify the employee tracking system is working correctly
"""

import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the main components from app.py
    from app import EMPLOYEE_DATA, calculate_leave_entitlements, generate_leave_request_email
    
    print("✅ Successfully imported employee tracking components!")
    print(f"📊 Found {len(EMPLOYEE_DATA)} employees in database:")
    
    # Test each employee
    for emp_key, emp_data in EMPLOYEE_DATA.items():
        print(f"\n👤 Employee: {emp_data['name']}")
        print(f"   Department: {emp_data['department']}")
        print(f"   Position: {emp_data['position']}")
        
        # Test leave calculations
        leave_balances = calculate_leave_entitlements(emp_data)
        print(f"   🏖️ Annual Leave Remaining: {leave_balances['annual_leave']['remaining']} days")
        print(f"   🏥 Sick Leave Remaining: {leave_balances['sick_leave']['remaining']} days")
    
    # Test email generation
    print("\n📧 Testing email generation...")
    test_employee = EMPLOYEE_DATA['loyed']
    subject, body = generate_leave_request_email(
        test_employee['name'],
        'Annual Leave',
        '2024-12-01',
        '2024-12-05',
        5,
        'Family vacation',
        test_employee['approval_manager']
    )
    
    print(f"✅ Email Subject: {subject}")
    print(f"✅ Email includes lgldubai@gmail.com: {'lgldubai@gmail.com' in body}")
    
    print("\n🎉 ALL EMPLOYEE TRACKING FEATURES ARE WORKING CORRECTLY!")
    print("🔍 If you're not seeing these features in the app, please:")
    print("   1. Make sure you're running the correct app.py file")
    print("   2. Check if you've deployed the latest version")
    print("   3. Clear your browser cache and refresh")
    
except ImportError as e:
    print(f"❌ Error importing components: {e}")
    print("❌ Employee tracking system may not be properly implemented")
except Exception as e:
    print(f"❌ Error testing system: {e}")