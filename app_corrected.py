import streamlit as st
import re
import time
import random
import pandas as pd
from datetime import datetime, date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
import json

# Configure the page
st.set_page_config(
    page_title="LGL Employee Helper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS styling with ALL UI improvements
st.markdown("""
<style>
    /* Main header styling with blue background and white text */
    .main-header {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem !important;
        margin: 0 !important;
    }
    
    .main-header p {
        color: white !important;
        opacity: 0.9 !important;
    }
    
    /* Button styling - blue background with white text */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 70px !important;
        box-shadow: 0 3px 10px rgba(52, 152, 219, 0.3) !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #1f4e79 100%) !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4) !important;
    }
    
    .stButton > button:focus {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        color: white !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5) !important;
    }
    
    /* Main content selectbox styling */
    .stSelectbox > div > div {
        background-color: white !important;
        color: #4a5568 !important;
        border: 2px solid #3498db !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stSelectbox label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Selectbox dropdown styling */
    .stSelectbox > div > div > div {
        color: #4a5568 !important;
    }
    
    .stSelectbox option {
        color: #4a5568 !important;
        background-color: white !important;
    }
    
    /* Sidebar selectbox styling - FIXED ALIGNMENT */
    div[data-testid="stSidebar"] .stSelectbox > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: white !important;
        color: #4a5568 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 0.375rem 0.75rem !important;
        font-size: 0.875rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: #4a5568 !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox label {
        color: #2d3748 !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Sidebar selectbox dropdown options */
    div[data-testid="stSidebar"] .stSelectbox option {
        color: #4a5568 !important;
        background-color: white !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #4a5568 !important;
        border: 2px solid #3498db !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: #4a5568 !important;
        border: 2px solid #3498db !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stTextArea label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Chat message styling */
    .bot-message {
        background: #f8f9fa !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border-left: 4px solid #3498db !important;
        margin: 1rem 0 !important;
        color: #2c3e50 !important;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.1) !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        text-align: right !important;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2) !important;
    }
    
    /* Form styling */
    .stForm {
        background: #f8f9fa !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 2px solid #e9ecef !important;
        margin: 1rem 0 !important;
    }
    
    /* Metric styling */
    .stMetric {
        background: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #e9ecef !important;
        text-align: center !important;
    }
    
    .stMetric label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: #3498db !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar button styling */
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
    }
    
    /* Responsive and alignment fixes */
    .element-container {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Fix column overflow issues */
    .row-widget {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ensure sidebar elements don't overflow */
    div[data-testid="stSidebar"] .element-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-size: 0.875rem !important;
        }
        
        .main-header h1 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            height: 60px !important;
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Employee Database - Sample Data for Leave Tracking
EMPLOYEE_DATA = {
    'loyed': {
        'name': 'Loyed',
        'department': 'Logistics',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP001',
        'join_date': '2023-01-15',
        'contract_type': 'Unlimited',
        'position': 'Logistics Coordinator',
        'annual_leave_taken': 10,
        'sick_leave_taken': 2,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 1.8
    },
    'eva': {
        'name': 'Eva',
        'department': 'Commercial Services',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP002',
        'join_date': '2022-08-10',
        'contract_type': 'Unlimited',
        'position': 'Commercial Services Specialist',
        'annual_leave_taken': 12,
        'sick_leave_taken': 3,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 2.3
    },
    'jaq': {
        'name': 'Jaq',
        'department': 'Commercial Sales',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP003',
        'join_date': '2024-01-20',
        'contract_type': 'Limited',
        'position': 'Sales Executive',
        'annual_leave_taken': 5,
        'sick_leave_taken': 7,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 0.7
    },
    'rajeev': {
        'name': 'Rajeev',
        'department': 'Vessel Operations',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP004',
        'join_date': '2021-05-03',
        'contract_type': 'Unlimited',
        'position': 'Operations Manager',
        'annual_leave_taken': 4,
        'sick_leave_taken': 6,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 5,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 3.6
    },
    'sarah': {
        'name': 'Sarah',
        'department': 'Human Resources',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP005',
        'join_date': '2020-11-12',
        'contract_type': 'Unlimited',
        'position': 'HR Manager',
        'annual_leave_taken': 8,
        'sick_leave_taken': 1,
        'maternity_leave_taken': 45,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 3,
        'probation_completed': True,
        'years_of_service': 4.1
    },
    'ahmed': {
        'name': 'Ahmed',
        'department': 'Finance',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP006',
        'join_date': '2023-09-01',
        'contract_type': 'Limited',
        'position': 'Financial Analyst',
        'annual_leave_taken': 6,
        'sick_leave_taken': 0,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 1.3
    }
}

def calculate_leave_entitlements(employee_data):
    """Calculate leave entitlements based on employee data and handbook policies"""
    years_of_service = employee_data['years_of_service']
    probation_completed = employee_data['probation_completed']
    
    # Annual Leave Calculation
    if years_of_service >= 1:
        annual_leave_entitlement = 22  # Subsequent years
    else:
        annual_leave_entitlement = 20  # First year
    
    # Sick Leave Calculation (only after probation)
    if probation_completed:
        sick_leave_entitlement = 90  # 90 calendar days per year
    else:
        sick_leave_entitlement = 0
    
    # Other leave entitlements
    maternity_leave_entitlement = 60 if employee_data['name'] else 60  # All female employees
    parental_leave_entitlement = 5  # Both male and female
    bereavement_leave_entitlement = 5  # Maximum for spouse
    
    return {
        'annual_leave': {
            'entitlement': annual_leave_entitlement,
            'taken': employee_data['annual_leave_taken'],
            'remaining': annual_leave_entitlement - employee_data['annual_leave_taken']
        },
        'sick_leave': {
            'entitlement': sick_leave_entitlement,
            'taken': employee_data['sick_leave_taken'],
            'remaining': sick_leave_entitlement - employee_data['sick_leave_taken']
        },
        'maternity_leave': {
            'entitlement': maternity_leave_entitlement,
            'taken': employee_data['maternity_leave_taken'],
            'remaining': maternity_leave_entitlement - employee_data['maternity_leave_taken']
        },
        'parental_leave': {
            'entitlement': parental_leave_entitlement,
            'taken': employee_data['parental_leave_taken'],
            'remaining': parental_leave_entitlement - employee_data['parental_leave_taken']
        },
        'bereavement_leave': {
            'entitlement': bereavement_leave_entitlement,
            'taken': employee_data['bereavement_leave_taken'],
            'remaining': bereavement_leave_entitlement - employee_data['bereavement_leave_taken']
        }
    }