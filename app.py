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
    .main-header {
        background: linear-gradient(135deg, rgb(52, 152, 219) 0%, rgb(41, 128, 185) 100%) !important;
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
    
    .stButton > button {
        background: linear-gradient(135deg, rgb(52, 152, 219) 0%, rgb(41, 128, 185) 100%) !important;
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
        background: linear-gradient(135deg, rgb(41, 128, 185) 0%, rgb(31, 78, 121) 100%) !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4) !important;
    }
    
    .stButton > button:focus {
        background: linear-gradient(135deg, rgb(52, 152, 219) 0%, rgb(41, 128, 185) 100%) !important;
        color: white !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5) !important;
    }
    
    .stSelectbox > div > div {
        background-color: white !important;
        color: rgb(74, 85, 104) !important;
        border: 2px solid rgb(52, 152, 219) !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stSelectbox label {
        color: rgb(45, 55, 72) !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox > div > div > div {
        color: rgb(74, 85, 104) !important;
    }
    
    .stSelectbox option {
        color: rgb(74, 85, 104) !important;
        background-color: white !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: white !important;
        color: rgb(74, 85, 104) !important;
        border: 1px solid rgb(226, 232, 240) !important;
        border-radius: 6px !important;
        padding: 0.375rem 0.75rem !important;
        font-size: 0.875rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: rgb(74, 85, 104) !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox label {
        color: rgb(45, 55, 72) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    div[data-testid="stSidebar"] .stSelectbox option {
        color: rgb(74, 85, 104) !important;
        background-color: white !important;
    }
    
    .stTextInput > div > div > input {
        background-color: white !important;
        color: rgb(74, 85, 104) !important;
        border: 2px solid rgb(52, 152, 219) !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput label {
        color: rgb(45, 55, 72) !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: rgb(74, 85, 104) !important;
        border: 2px solid rgb(52, 152, 219) !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stTextArea label {
        color: rgb(45, 55, 72) !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stDateInput > div > div > input {
        background-color: white !important;
        color: rgb(74, 85, 104) !important;
        border: 2px solid rgb(52, 152, 219) !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stDateInput label {
        color: rgb(45, 55, 72) !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .bot-message {
        background: rgb(248, 249, 250) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border-left: 4px solid rgb(52, 152, 219) !important;
        margin: 1rem 0 !important;
        color: rgb(44, 62, 80) !important;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.1) !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgb(52, 152, 219), rgb(41, 128, 185)) !important;
        color: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        text-align: right !important;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2) !important;
    }
    
    .stForm {
        background: rgb(248, 249, 250) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 2px solid rgb(233, 236, 239) !important;
        margin: 1rem 0 !important;
    }
    
    .stMetric {
        background: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid rgb(233, 236, 239) !important;
        text-align: center !important;
    }
    
    .stMetric label {
        color: rgb(44, 62, 80) !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: rgb(52, 152, 219) !important;
        font-weight: 700 !important;
    }
    
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, rgb(52, 152, 219) 0%, rgb(41, 128, 185) 100%) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
    }
    
    .element-container {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    .row-widget {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    div[data-testid="stSidebar"] .element-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 0 !important;
    }
    
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

def create_notification_links(form_type, employee_name, manager_name, form_data):
    """Create various notification service links for sending requests"""
    email_subject = f"{form_type} Request - {employee_name}"
    
    # Create email body
    email_body = f"""Dear {manager_name},

I would like to submit a {form_type} request:

REQUEST DETAILS:
• Employee: {employee_name}
• Request Type: {form_type}
• Date: {datetime.now().strftime('%B %d, %Y')}
"""
    
    for key, value in form_data.items():
        if key not in ['employee_name', 'manager_name', 'form_type']:
            formatted_key = key.replace('_', ' ').title()
            email_body += f"• {formatted_key}: {value}\n"
    
    email_body += f"""

Please review and approve this request.

Best regards,
{employee_name}

Generated by LGL Employee Helper
Alistar Personnel"""
    
    # URL encode for links
    subject_encoded = urllib.parse.quote(email_subject)
    body_encoded = urllib.parse.quote(email_body)
    manager_email = "concessioac@gmail.com"
    
    return {
        'gmail_url': f"https://mail.google.com/mail/?view=cm&to={manager_email}&subject={subject_encoded}&body={body_encoded}",
        'outlook_url': f"https://outlook.live.com/mail/0/deeplink/compose?to={manager_email}&subject={subject_encoded}&body={body_encoded}",
        'yahoo_url': f"https://compose.mail.yahoo.com/?to={manager_email}&subject={subject_encoded}&body={body_encoded}",
        'subject': email_subject,
        'body': email_body,
        'manager_email': manager_email
    }

def generate_email_alternatives(form_type, employee_name, manager_name, form_data):
    """Generate multiple email alternatives for form submission"""
    email_subject = f"{form_type} Request - {employee_name}"
    
    # Simple text email for copying
    text_email = f"""Subject: {email_subject}
To: concessioac@gmail.com

Dear {manager_name},

I would like to submit a {form_type} request with the following details:

📋 REQUEST DETAILS:
• Employee: {employee_name}
• Request Type: {form_type}
• Date Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
• Status: Pending Approval
"""
    
    # Add form-specific details
    for key, value in form_data.items():
        if key not in ['employee_name', 'manager_name', 'form_type']:
            formatted_key = key.replace('_', ' ').title()
            text_email += f"• {formatted_key}: {value}\n"
    
    text_email += f"""

Please review this request and let me know your decision.

For approval, please reply with: APPROVED - {form_type} Request - {employee_name}
For rejection, please reply with: REJECTED - {form_type} Request - {employee_name}

Thank you for your consideration.

Best regards,
{employee_name}

---
This request was generated by the LGL Employee Helper System
Alistar Personnel | 605, Park Avenue, Dubai Silicon Oasis
HR Contact: concessioac@gmail.com"""
    
    # Mailto URL for email clients
    mailto_url = f"mailto:concessioac@gmail.com?subject={email_subject.replace(' ', '%20')}&body={text_email.replace(' ', '%20').replace('\n', '%0A')}"
    
    # WhatsApp message format
    whatsapp_message = f"""*{form_type} Request - {employee_name}*

Dear {manager_name},

I would like to submit a {form_type} request:

📋 *REQUEST DETAILS:*
• Employee: {employee_name}
• Request Type: {form_type}
• Date: {datetime.now().strftime('%B %d, %Y')}
"""
    
    for key, value in form_data.items():
        if key not in ['employee_name', 'manager_name', 'form_type']:
            formatted_key = key.replace('_', ' ').title()
            whatsapp_message += f"• {formatted_key}: {value}\n"
    
    whatsapp_message += f"""

Please review and approve.

Thanks,
{employee_name}

_Generated by LGL Employee Helper_"""
    
    return {
        'subject': email_subject,
        'text_email': text_email,
        'mailto_url': mailto_url,
        'whatsapp_message': whatsapp_message
    }

# Form Types Configuration
FORM_TYPES = {
    'leave_request': {
        'title': '🏖️ Leave Request',
        'description': 'Request time off for vacation, sick leave, maternity, etc.',
        'icon': '🏖️',
        'fields': ['leave_type', 'start_date', 'end_date', 'reason', 'emergency_contact']
    },
    'visa_request': {
        'title': '📋 Visa & Immigration Request',
        'description': 'Request visa sponsorship or dependent visa support',
        'icon': '📋',
        'fields': ['visa_type', 'dependent_details', 'urgency', 'reason']
    },
    'health_insurance': {
        'title': '🏥 Health Insurance Request',
        'description': 'Request health insurance changes or dependent coverage',
        'icon': '🏥',
        'fields': ['insurance_type', 'dependent_info', 'medical_history', 'preferred_provider']
    },
    'performance_review': {
        'title': '📈 Performance Review Request',
        'description': 'Request performance appraisal or schedule review meeting',
        'icon': '📈',
        'fields': ['review_type', 'preferred_date', 'self_assessment', 'goals']
    },
    'training_request': {
        'title': '🎓 Training & Development Request',
        'description': 'Request professional development or training opportunities',
        'icon': '🎓',
        'fields': ['training_type', 'course_name', 'provider', 'cost_estimate', 'justification']
    },
    'grievance_report': {
        'title': '⚠️ Grievance Report',
        'description': 'Report workplace issues or file a formal complaint',
        'icon': '⚠️',
        'fields': ['issue_type', 'incident_date', 'involved_parties', 'description', 'witnesses']
    },
    'equipment_request': {
        'title': '💻 Equipment Request',
        'description': 'Request office equipment, technology, or supplies',
        'icon': '💻',
        'fields': ['equipment_type', 'specification', 'justification', 'urgency']
    },
    'policy_clarification': {
        'title': '📜 Policy Clarification Request',
        'description': 'Request clarification on company policies or procedures',
        'icon': '📜',
        'fields': ['policy_area', 'specific_question', 'situation_context']
    },
    'schedule_change': {
        'title': '⏰ Schedule Change Request',
        'description': 'Request changes to working hours or schedule',
        'icon': '⏰',
        'fields': ['change_type', 'proposed_schedule', 'effective_date', 'reason']
    },
    'resignation_notice': {
        'title': '📝 Resignation Notice',
        'description': 'Submit formal resignation and notice period',
        'icon': '📝',
        'fields': ['last_working_day', 'notice_period', 'reason', 'transition_plan']
    }
}

# Main header with blue background and white text
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem; color: white;">🤖 LGL Employee Helper</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9; color: white;">Alistar's Personnel Employee Handbook</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'selected_employee' not in st.session_state:
    st.session_state.selected_employee = None
if 'current_form' not in st.session_state:
    st.session_state.current_form = None

# Sidebar for employee selection
with st.sidebar:
    st.markdown("### Employee Portal")
    
    # Employee selection dropdown
    employee_options = ["Select Employee"] + [emp_data['name'] for emp_data in EMPLOYEE_DATA.values()]
    selected_employee = st.selectbox(
        "Choose your name:",
        employee_options,
        index=0 if st.session_state.selected_employee is None else employee_options.index(st.session_state.selected_employee) if st.session_state.selected_employee in employee_options else 0
    )
    
    if selected_employee != "Select Employee":
        st.session_state.selected_employee = selected_employee
        
        # Find employee data
        employee_key = None
        for key, data in EMPLOYEE_DATA.items():
            if data['name'] == selected_employee:
                employee_key = key
                break
        
        if employee_key:
            employee_data = EMPLOYEE_DATA[employee_key]
            st.markdown(f"**Welcome, {employee_data['name']}!**")
            st.markdown(f"**Department:** {employee_data['department']}")
            st.markdown(f"**Position:** {employee_data['position']}")
            st.markdown(f"**Employee ID:** {employee_data['employee_id']}")
            
            # Calculate and show leave balances
            leave_data = calculate_leave_entitlements(employee_data)
            
            st.markdown("---")
            st.markdown("### Leave Balance")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Annual Leave", f"{leave_data['annual_leave']['remaining']} days", 
                         delta=f"Used: {leave_data['annual_leave']['taken']}")
            with col2:
                st.metric("Sick Leave", f"{leave_data['sick_leave']['remaining']} days", 
                         delta=f"Used: {leave_data['sick_leave']['taken']}")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # HOW CAN I APPLY FOR LEAVE section with bigger buttons
    st.markdown("### 📋 How can I apply for leave?")
    st.markdown("Choose the type of request you'd like to make:")
    
    # Create bigger buttons in a 2x5 grid
    form_keys = list(FORM_TYPES.keys())
    for i in range(0, len(form_keys), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(form_keys):
                form_key = form_keys[i + j]
                form_config = FORM_TYPES[form_key]
                with col:
                    if st.button(
                        f"{form_config['icon']} {form_config['title']}", 
                        key=f"form_{form_key}",
                        help=form_config['description']
                    ):
                        st.session_state.current_form = form_key
                        st.rerun()

# Display form if one is selected
if st.session_state.current_form and st.session_state.selected_employee:
    form_config = FORM_TYPES[st.session_state.current_form]
    
    st.markdown("---")
    st.markdown(f"## {form_config['title']}")
    st.markdown(f"*{form_config['description']}*")
    
    # Find employee data
    employee_key = None
    for key, data in EMPLOYEE_DATA.items():
        if data['name'] == st.session_state.selected_employee:
            employee_key = key
            break
    
    if employee_key:
        employee_data = EMPLOYEE_DATA[employee_key]
        
        with st.form(f"form_{st.session_state.current_form}"):
            form_data = {}
            
            # Basic employee info
            st.markdown("### Employee Information")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Employee Name", value=employee_data['name'], disabled=True)
            with col2:
                st.text_input("Department", value=employee_data['department'], disabled=True)
            
            # Form-specific fields
            st.markdown("### Request Details")
            
            if st.session_state.current_form == 'leave_request':
                col1, col2 = st.columns(2)
                with col1:
                    leave_type = st.selectbox("Leave Type", 
                        ["Annual Leave", "Sick Leave", "Maternity Leave", "Parental Leave", "Bereavement Leave", "Emergency Leave"])
                    start_date = st.date_input("Start Date", value=datetime.now().date())
                with col2:
                    end_date = st.date