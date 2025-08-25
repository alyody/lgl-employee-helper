import streamlit as st
import re
import time
import random
import pandas as pd
from datetime import datetime, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure the page
st.set_page_config(
    page_title="LGL Employee Helper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

def generate_form_email(form_type, employee_name, manager_name, form_data):
    """Generate a formatted email for various form types with HTML formatting"""
    email_subject = f"{form_type} Request - {employee_name}"
    
    # HTML Email Template
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #2c3e50, #3498db); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .header p {{ margin: 5px 0 0 0; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .form-details {{ background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-row {{ margin: 10px 0; display: flex; }}
        .detail-label {{ font-weight: bold; min-width: 150px; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .action-buttons {{ text-align: center; margin: 30px 0; }}
        .approve-btn {{ background-color: #27ae60; color: white; padding: 12px 24px; border: none; border-radius: 5px; margin: 0 10px; text-decoration: none; display: inline-block; font-weight: bold; }}
        .reject-btn {{ background-color: #e74c3c; color: white; padding: 12px 24px; border: none; border-radius: 5px; margin: 0 10px; text-decoration: none; display: inline-block; font-weight: bold; }}
        .footer {{ background-color: #34495e; color: white; padding: 20px; text-align: center; font-size: 12px; }}
        .status {{ display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; background-color: #f39c12; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 Alistar Personnel</h1>
            <p>{form_type} Request Approval</p>
        </div>
        
        <div class="content">
            <h2>Dear {manager_name},</h2>
            <p>You have received a new <strong>{form_type}</strong> request that requires your approval.</p>
            
            <div class="form-details">
                <h3>📋 Request Details</h3>
                <div class="detail-row">
                    <span class="detail-label">Employee:</span>
                    <span class="detail-value">{employee_name}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Request Type:</span>
                    <span class="detail-value">{form_type}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Date Submitted:</span>
                    <span class="detail-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    <span class="status">Pending Approval</span>
                </div>
"""
    
    # Add form-specific details
    for key, value in form_data.items():
        if key not in ['employee_name', 'manager_name', 'form_type']:
            formatted_key = key.replace('_', ' ').title()
            html_template += f"""
                <div class="detail-row">
                    <span class="detail-label">{formatted_key}:</span>
                    <span class="detail-value">{value}</span>
                </div>"""
    
    html_template += f"""
            </div>
            
            <div class="action-buttons">
                <a href="mailto:concessioac@gmail.com?subject=APPROVED - {form_type} Request - {employee_name}&body=Dear {employee_name},%0A%0AYour {form_type} request has been APPROVED.%0A%0AApproval Details:%0A• Approved by: {manager_name}%0A• Approval Date: {datetime.now().strftime('%Y-%m-%d')}%0A• Comments: [Add any comments here]%0A%0APlease contact HR if you have any questions.%0A%0ABest regards,%0A{manager_name}" class="approve-btn">✅ APPROVE</a>
                
                <a href="mailto:concessioac@gmail.com?subject=REJECTED - {form_type} Request - {employee_name}&body=Dear {employee_name},%0A%0AYour {form_type} request has been REJECTED.%0A%0ARejection Details:%0A• Rejected by: {manager_name}%0A• Rejection Date: {datetime.now().strftime('%Y-%m-%d')}%0A• Reason: [Please provide reason here]%0A%0APlease contact me if you have any questions or would like to discuss this further.%0A%0ABest regards,%0A{manager_name}" class="reject-btn">❌ REJECT</a>
            </div>
            
            <p><strong>Instructions:</strong></p>
            <ul>
                <li>Click the appropriate button above to approve or reject this request</li>
                <li>An email will be automatically generated to notify the employee</li>
                <li>Please add any additional comments before sending</li>
                <li>For questions, contact HR at concessioac@gmail.com</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>📧 This request was generated by the LGL Employee Helper System</p>
            <p>Alistar Personnel | 605, Park Avenue, Dubai Silicon Oasis</p>
        </div>
    </div>
</body>
</html>"""
    
    return email_subject, html_template

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
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        color: white;
        margin-left: 2rem;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .option-button {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #2196f3;
        padding: 12px 24px;
        border-radius: 25px;
        margin: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #1976d2;
        font-size: 16px;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.2);
    }
    
    .option-button:hover {
        background: linear-gradient(135deg, #2196f3, #1976d2);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(33, 150, 243, 0.4);
    }
    
    .quick-action {
        background: linear-gradient(135deg, #ecf0f1, #bdc3c7);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .quick-action:hover {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .choice-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Employee Handbook Data
HANDBOOK_DATA = {
    'leave': {
        'title': 'Annual Leave Policy',
        'content': """📅 **Annual Leave Entitlement:**

• **First Year:** 20 working days (after probation completion)
• **Subsequent Years:** 22 working days from second year onward
• **Notice Required:** Minimum twice the duration of leave requested
• **Peak Periods:** July and August may have restrictions

**How to Apply:**
1. Submit Annual Leave Form to Line Manager
2. First-come, first-served basis
3. Subject to operational requirements

**Carry Over Rules:**
• Administrative Staff: Maximum 7 days per year
• Teaching Staff: Not permitted to carry over

📋 **Reference:** Section 9.2 of Employee Handbook"""
    },
    
    'sick': {
        'title': 'Sick Leave Policy',
        'content': """🏥 **Sick Leave Entitlement (per year):**

• **Total:** 90 calendar days after 3 months post-probation
• **Full Pay:** First 15 calendar days
• **Half Pay:** Next 30 calendar days
• **No Pay:** Next 45 days

**Application Process:**
• Notify manager within 1.5 hours (academic) or 1 hour (admin)
• Complete Sick Leave Form upon return
• Medical certificate required for absence beyond 2 days

⚠️ **Important:** Available only after completing probationary period

📋 **Reference:** Section 9.3 of Employee Handbook"""
    },
    
    'working hours': {
        'title': 'Working Hours',
        'content': """⏰ **Working Hours:**

**Administrative Staff:**
• Days: Monday – Friday
• Hours: 9:00am – 6:00pm
• Overtime: Paid at management's discretion

**Academic Staff:**
• Days: Monday to Friday
• Sessions: 9am-12pm, 12pm-3pm, 3pm-6pm
• Minimum: 2 sessions per day
• Flexible scheduling based on demand

**Ramadan Hours:**
• 2 hours reduction per day (if normal hours exceed 8 hours)
• 1 week notice for revised times
• Applies to administrative staff only

📋 **Reference:** Section 5 of Employee Handbook"""
    },
    
    'benefits': {
        'title': 'Employee Benefits',
        'content': """🎁 **Comprehensive Benefits Package:**

**Health Insurance:**
• Basic Cover: First 6 months (probation)
• Comprehensive Cover: After 6 months

**Visa Sponsorship:**
• Company-sponsored resident visa
• Dependent visas available (employee covers costs)

**Leave Benefits:**
• Annual Leave: 20-22 days
• Sick Leave: Up to 90 days
• Maternity: 60 days (45 full pay + 15 half pay)
• Parental: 5 days (male/female)
• Bereavement: 3-5 days

**National Holidays:**
• New Year's Day • Eid Al Fitr (2 days) • Eid Al Adha (3 days)
• Prophet's Birthday • National Day • Isra & Al Miraj

📋 **Reference:** Section 9 of Employee Handbook"""
    },
    
    'conduct': {
        'title': 'Code of Conduct',
        'content': """👔 **Professional Standards:**

**Employee Duties:**
• Create culture of mutual respect
• Exercise reasonable skill and care
• Maintain confidentiality
• Professional language at all times
• Healthy work-life balance

**Dress Code:**
• Smart, professional attire
• Clean, tidy, and appropriate clothing
• Cover tattoos where possible
• No torn, transparent, or inappropriate clothing
• Religious dress permitted unless safety risk

**Safeguarding (Students):**
• No physical contact with students
• Avoid being alone with students
• Maintain professional boundaries
• No personal relationships
• Report any concerns to management

📋 **Reference:** Section 6 of Employee Handbook"""
    },
    
    'disciplinary': {
        'title': 'Disciplinary Procedures',
        'content': """⚖️ **Disciplinary Process:**

**Warning System:**
• Verbal Warning: 6 months validity
• First Written: 12 months validity
• Final Written: 12 months validity

**Minor Misconduct Examples:**
• Persistent lateness • Unauthorized absence
• Failure to follow procedures • Private work during hours

**Gross Misconduct Examples:**
• Theft of company property • Breach of confidentiality
• Being unfit for duty • Safeguarding violations
• Discrimination/harassment • Bringing company into disrepute

**Process:**
1. Formal investigation by HR
2. Written notification of hearing
3. Disciplinary hearing with representation
4. Decision communicated in writing
5. Right to appeal within 5 days

📋 **Reference:** Section 12 of Employee Handbook"""
    },
    
    'covid': {
        'title': 'COVID-19 Policy',
        'content': """🦠 **COVID-19 Guidelines:**

**If Showing Symptoms:**
• Immediate isolation and hospital referral
• Cannot return until PCR result obtained
• 7-day quarantine for close contacts

**Vaccination Requirements:**
• Proof of vaccination required
• Weekly PCR tests if unvaccinated
• Medical exemptions with doctor's certificate

**Workplace Protocols:**
• Regular sanitization
• Social distancing measures
• Online teaching capabilities for quarantine

📋 **Reference:** Section 10 of Employee Handbook"""
    },
    
    'termination': {
        'title': 'Termination & Gratuity',
        'content': """📋 **End of Service:**

**Notice Periods:**
• Limited Contract: No notice (expires at end date)
• Unlimited Contract: Minimum 30 calendar days

**Gratuity Calculation:**
• 21 days basic pay for each of first 5 years
• 30 days basic pay for each additional year
• Maximum: 2 years' total pay

**Early Termination:**
• Employer: 3 months' compensation
• Employee: Half of 3 months' compensation

**Resignation Gratuity (Unlimited Contract):**
• 1-3 years: 2/3 reduction
• 3-5 years: 1/3 reduction
• 5+ years: No reduction

📋 **Reference:** Section 18 of Employee Handbook"""
    },
    
    # New sub-category entries
    'health insurance': {
        'title': 'Health Insurance Coverage',
        'content': """🏥 **Health Insurance Policy:**

**Coverage Levels:**
• **Probation Period:** Basic medical coverage (first 6 months)
• **After 6 Months:** Comprehensive medical coverage
• **Dependents:** Available upon request (employee covers costs)

**What's Covered:**
• Medical consultations and treatments
• Emergency medical services
• Prescription medications
• Specialist referrals

**Important Notes:**
• Coverage begins after probation completion
• Employee responsible for dependent insurance costs
• Processing fees apply for dependent coverage

📋 **Reference:** Section 9 of Employee Handbook"""
    },
    
    'visa sponsorship': {
        'title': 'Visa & Immigration Support',
        'content': """📋 **Visa Sponsorship Policy:**

**Employee Visa:**
• Company-sponsored resident visa provided
• All visa processing handled by company
• Valid for duration of employment

**Dependent Visas:**
• Available upon request and line manager agreement
• Employee covers ALL dependent costs including:
  - Processing fees
  - Visa application fees  
  - Medical insurance for dependents
  - Emirates ID fees

**Application Process:**
• Submit request to line manager
• Provide required documentation
• Company assists with processing

📋 **Reference:** Section 9 of Employee Handbook"""
    },
    
    'national holidays': {
        'title': 'National Holidays & Public Days Off',
        'content': """🎆 **Official National Holidays:**

**Religious Holidays:**
• Hijiri's New Year's Day (1 day)
• Eid Al Fitr (2 days)
• Eid Al Adha (3 days)
• Prophet Mohammed's Birthday (1 day)
• Isra and Al Miraj (1 day)

**National Celebrations:**
• Gregorian New Year's Day (1 day)
• UAE National Day (1 day)

**Total:** 9 official national holidays per year

**Important Notes:**
• Holidays are paid time off
• Dates may vary based on lunar calendar
• Official announcements will be made
• No work required on these days

📋 **Reference:** Section 9 of Employee Handbook"""
    },
    
    'administrative hours': {
        'title': 'Administrative Staff Working Hours',
        'content': """💼 **Administrative Staff Schedule:**

**Regular Hours:**
• **Days:** Monday – Friday
• **Time:** 9:00am – 6:00pm
• **Break:** Standard lunch break included

**Overtime:**
• Paid in accordance to confirmed attendance
• At management's discretion
• Must be pre-approved

**Ramadan Schedule:**
• 2 hours reduction per day (if normal hours exceed 8 hours)
• 1 week notice provided for revised times
• Applies to administrative staff only

**Attendance:**
• Punctuality expected
• Notify manager of any delays
• Consistent lateness may result in disciplinary action

📋 **Reference:** Section 5 of Employee Handbook"""
    },
    
    'academic hours': {
        'title': 'Academic Staff Teaching Schedule',
        'content': """🏫 **Academic Staff Schedule:**

**Teaching Sessions:**
• **Morning:** 9:00am – 12:00pm
• **Afternoon:** 12:00pm – 3:00pm  
• **Evening:** 3:00pm – 6:00pm

**Requirements:**
• **Minimum:** 2 sessions per day
• **Days:** Monday to Friday
• **Flexibility:** Can work additional sessions based on demand

**Schedule Variations:**
• Can work 3rd session during busy periods (overtime)
• May reduce to 1 session during quieter periods
• Schedule adjustments based on student enrollment

**Ramadan:**
• No special hour reductions for teaching staff
• Maintain regular session schedule

📋 **Reference:** Section 5 of Employee Handbook"""
    },
    
    'dress code': {
        'title': 'Professional Dress Code Standards',
        'content': """👔 **Dress Code Policy:**

**Required Standards:**
• Smart, professional attire
• Clean, tidy, and appropriate clothing
• Professional appearance at all times

**Prohibited Items:**
• Torn, dirty, or worn clothing/footwear
• Transparent clothing revealing underwear or midriffs
• Low-cut necklines
• Very short skirts or trousers
• Shorts or beachwear
• Flip-flops

**Personal Appearance:**
• **Tattoos:** Should be covered where possible
• **Piercings:** Only earrings or nose studs permitted
• **Religious dress:** Appropriate cultural dress permitted unless safety risk

**Compliance:**
• Managers may address dress code violations
• Repeated violations may result in disciplinary action

📋 **Reference:** Section 6 of Employee Handbook"""
    },
    
    'safeguarding rules': {
        'title': 'Student Safeguarding Guidelines',
        'content': """🛑 **Student Safeguarding Policy:**

**Physical Contact:**
• **No physical contact** with students
• Maintain professional distance at all times
• Avoid situations that could be misinterpreted

**Interaction Guidelines:**
• Avoid being alone with students
• Keep classroom doors open
• Maintain respectable distance
• No personal conversations with students
• No advice about personal relationships

**Teaching Environment:**
• No teaching small groups without another staff member present
• Be aware of student attachments and maintain distance
• Report any concerning behavior to management

**Outside Contact:**
• **No contact outside school**
• No personal contact details to students
• No social media following (except official ES forums)
• No private meetings outside school
• No vehicle lifts without permission
• No private parties or social events
• **No romantic or sexual relationships with students**

**Violations:**
• Safeguarding violations are considered **gross misconduct**
• May result in immediate termination

📋 **Reference:** Section 6 of Employee Handbook"""
    },
    
    'minor misconduct': {
        'title': 'Minor Misconduct Examples & Consequences',
        'content': """⚠️ **Minor Misconduct Categories:**

**Attendance Issues:**
• Persistent lateness and poor timekeeping
• Unauthorized absence without valid reason
• Abuse of sick leave policies

**Work Performance:**
• Incompetence in job duties
• Failure to follow prescribed procedures
• Failure to observe company regulations
• Private work during working hours

**Typical Consequences:**
• **First Offense:** Verbal warning (6 months validity)
• **Repeated Issues:** First written warning (12 months validity)
• **Continued Problems:** Final written warning (12 months validity)
• **Persistent Issues:** Possible termination

**Progressive Discipline:**
• Warnings build upon each other
• Each step gives opportunity for improvement
• Support and training may be provided
• Right to appeal at each stage

📋 **Reference:** Section 12 of Employee Handbook"""
    },
    
    'gross misconduct': {
        'title': 'Gross Misconduct & Immediate Consequences',
        'content': """🚨 **Serious Violations (Gross Misconduct):**

**Criminal/Illegal Acts:**
• Theft or unauthorized possession of company property
• Bribery, corruption, or illegal activities
• Physical assault or threats of violence

**Professional Violations:**
• Breaches of confidentiality or security
• Being unfit for duty due to drugs/alcohol
• False declaration of qualifications
• Failure to observe safeguarding rules

**Workplace Behavior:**
• Refusal to carry out management instructions
• Insulting behavior/insubordination
• Unlawful discrimination, bullying, or harassment
• Bringing organization into serious disrepute
• Willful damage of company property
• Intimidation of colleagues or students

**Technology Misuse:**
• Accessing pornographic/offensive material
• Serious misuse of company IT systems

**Immediate Consequences:**
• **May result in immediate termination**
• No progressive warnings required
• Summary dismissal possible
• Right to formal hearing and appeal

📋 **Reference:** Section 12 of Employee Handbook"""
    },
    
    'performance appraisal': {
        'title': 'Performance Appraisal Process',
        'content': """📊 **Annual Performance Review:**

**Schedule:**
• **First Review:** After 6-month probation completion
• **Ongoing:** Annual formal reviews thereafter
• **Mid-Year:** Optional 6-month verbal review
• **Notice:** At least 1 week before meeting

**Review Process:**
• Performance evaluation forms provided in advance
• Employee self-assessment encouraged
• Meeting with line manager or senior staff
• Discussion of achievements and areas for improvement
• Goal setting for upcoming period

**Confidentiality:**
• Information shared only with senior management
• Private and confidential process
• Professional development focus

**Outcomes:**
• Performance rating
• Development plan
• Training recommendations
• Career progression discussions
• Salary review considerations

**Documentation:**
• Written record of review
• Signed by both parties
• Filed in personnel records

📋 **Reference:** Section 11 of Employee Handbook"""
    },
    
    'maternity leave': {
        'title': 'Maternity Leave Policy',
        'content': """🤱 **Maternity Leave Entitlement:**

**Total Leave:** 60 days
• **Full Pay:** First 45 consecutive calendar days
• **Half Pay:** Following 15 days

**Application Requirements:**
• **Notice:** 15 weeks before due date
• **Documentation:** Medical certificate required
• **Planning:** Coordinate with line manager

**Additional Benefits:**
• **Feeding Breaks:** Two additional 30-minute breaks each day
• **Duration:** Available for 18 months post-delivery
• **Extended Leave:** Up to 100 additional days without pay (consecutive or non-consecutive)

**Return to Work:**
• Medical clearance required
• Gradual return options available
• Job protection during leave period

**Important Notes:**
• Leave cannot be carried over
• Available to all female employees
• Coordinate with HR for smooth transition

📋 **Reference:** Section 9.4 of Employee Handbook"""
    },
    
    'parental leave': {
        'title': 'Parental Leave Policy',
        'content': """👶 **Parental Leave Entitlement:**

**For All New Parents:**
• **Female Employees:** 5 paid days
• **Male Employees:** 5 paid days
• **Time Frame:** Must be taken within 6 months of birth

**Application Process:**
• Submit request to line manager
• Provide birth certificate/documentation
• Can be taken consecutively or separately
• Advance notice preferred

**Purpose:**
• Support new parent bonding
• Assist with family adjustment
• Cover immediate post-birth needs
• Complement maternity leave for mothers

**Coverage:**
• Full salary maintained
• No impact on annual leave entitlement
• Job protection guaranteed
• Available for adoptions as well

**Coordination:**
• Work with team to cover responsibilities
• Plan ahead for smooth workflow
• Support available from management

📋 **Reference:** Section 9.5 of Employee Handbook"""
    },
    
    'bereavement leave': {
        'title': 'Bereavement Leave Policy',
        'content': """🕊 **Bereavement Leave Entitlement:**

**Spouse/Partner:**
• **5 paid days** for loss of spouse or life partner
• Can be taken consecutively or as needed
• Additional unpaid leave may be granted

**Immediate Family:**
• **3 paid days** for loss of:
  - Parent or step-parent
  - Child or step-child
  - Sibling
  - Grandchild
  - Grandparent

**Application Process:**
• Notify line manager as soon as possible
• No formal application required initially
• Documentation may be requested later
• Flexible timing based on funeral arrangements

**Additional Support:**
• Extended unpaid leave available if needed
• Flexible working arrangements during grief period
• Employee assistance program access
• Counseling support available

**Important:**
• Full salary maintained during paid leave
• No impact on other leave entitlements
• Cultural and religious considerations respected
• Management support available

📋 **Reference:** Section 9.6 of Employee Handbook"""
    }
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    welcome_response = {
        'type': 'content',
        'content': '👋 Hello! I am your **LGL Employee Helper**. Ask me anything about the Alistar Personnel Employee Handbook!\n\nI can help you with policies, procedures, benefits, and much more. What would you like to know?'
    }
    st.session_state.messages.append({
        'role': 'assistant',
        'content': welcome_response['content'],
        'response_data': welcome_response
    })

# Initialize employee session
if 'current_employee' not in st.session_state:
    st.session_state.current_employee = None
if 'employee_data' not in st.session_state:
    st.session_state.employee_data = None

# Initialize input tracking to prevent loops
if 'last_input' not in st.session_state:
    st.session_state.last_input = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False

def process_user_question(question):
    """Process user question and return appropriate response"""
    question_lower = question.lower().strip()
    
    # Check for employee-specific queries first
    if st.session_state.current_employee:
        employee_data = st.session_state.employee_data
        leave_balances = calculate_leave_entitlements(employee_data)
        
        # Check for leave balance queries
        if any(phrase in question_lower for phrase in ['my leave', 'leave balance', 'leave left', 'remaining leave', 'how many days']):
            return {
                'type': 'content',
                'content': f"""📅 **Your Leave Balance - {employee_data['name']}**

🏖️ **Annual Leave:**
• Entitled: {leave_balances['annual_leave']['entitlement']} days
• Used: {leave_balances['annual_leave']['taken']} days
• **Remaining: {leave_balances['annual_leave']['remaining']} days**

🏥 **Sick Leave:**
• Entitled: {leave_balances['sick_leave']['entitlement']} days
• Used: {leave_balances['sick_leave']['taken']} days
• **Remaining: {leave_balances['sick_leave']['remaining']} days**

🤱 **Maternity Leave:**
• Entitled: {leave_balances['maternity_leave']['entitlement']} days
• Used: {leave_balances['maternity_leave']['taken']} days
• **Remaining: {leave_balances['maternity_leave']['remaining']} days**

👶 **Parental Leave:**
• Entitled: {leave_balances['parental_leave']['entitlement']} days
• Used: {leave_balances['parental_leave']['taken']} days
• **Remaining: {leave_balances['parental_leave']['remaining']} days**

🕊 **Bereavement Leave:**
• Entitled: {leave_balances['bereavement_leave']['entitlement']} days
• Used: {leave_balances['bereavement_leave']['taken']} days
• **Remaining: {leave_balances['bereavement_leave']['remaining']} days**

💼 **Employee Information:**
• Department: {employee_data['department']}
• Manager: {employee_data['approval_manager']}
• Service Years: {employee_data['years_of_service']} years

📧 Would you like to request leave? Just ask me to 'request leave' and I'll help you generate an email!

*Have a great day! I am always here to guide you. Do you want to know more?* 😊"""
            }
        
        # Check for leave request queries
        if any(phrase in question_lower for phrase in ['request leave', 'apply for leave', 'leave request', 'book leave']):
            return {
                'type': 'leave_request',
                'content': f"""📧 **Leave Request Form - {employee_data['name']}**

I'll help you prepare a leave request email to send to your manager.

📅 **Your Current Leave Balances:**
• Annual Leave: {leave_balances['annual_leave']['remaining']} days remaining
• Sick Leave: {leave_balances['sick_leave']['remaining']} days remaining
• Maternity Leave: {leave_balances['maternity_leave']['remaining']} days remaining
• Parental Leave: {leave_balances['parental_leave']['remaining']} days remaining

Please use the form below to submit your leave request:""",
                'employee_data': employee_data,
                'leave_balances': leave_balances
            }
        
        # Check for specific leave balance queries
        if 'annual leave' in question_lower and any(word in question_lower for word in ['balance', 'left', 'remaining', 'how many']):
            remaining = leave_balances['annual_leave']['remaining']
            return {
                'type': 'content',
                'content': f"""🏖️ **Annual Leave Balance - {employee_data['name']}**

You have **{remaining} days** of annual leave remaining this year.

📅 **Details:**
• Total Entitlement: {leave_balances['annual_leave']['entitlement']} days
• Already Used: {leave_balances['annual_leave']['taken']} days
• **Available: {remaining} days**

📧 Would you like to request annual leave? Just ask me to 'request leave'!

*Have a great day! I am always here to guide you. Do you want to know more?* 😊"""
            }
            
        if 'sick leave' in question_lower and any(word in question_lower for word in ['balance', 'left', 'remaining', 'how many']):
            remaining = leave_balances['sick_leave']['remaining']
            return {
                'type': 'content',
                'content': f"""🏥 **Sick Leave Balance - {employee_data['name']}**

You have **{remaining} days** of sick leave remaining this year.

📅 **Details:**
• Total Entitlement: {leave_balances['sick_leave']['entitlement']} days
• Already Used: {leave_balances['sick_leave']['taken']} days
• **Available: {remaining} days**

⚠️ **Note:** Medical certificate required for absences over 2 days.

📧 Would you like to request sick leave? Just ask me to 'request leave'!

*Have a great day! I am always here to guide you. Do you want to know more?* 😊"""
            }
    
    # Define intuitive keyword mappings - more flexible matching
    keyword_mappings = {
        'annual_leave': {
            'keywords': ['annual leave', 'vacation', 'holiday', 'time off', 'days off', 'annual', 'holidays', 'vacations'],
            'icon': '🏖️',
            'title': 'Annual Leave'
        },
        'sick_leave': {
            'keywords': ['sick leave', 'medical leave', 'illness', 'doctor', 'health leave', 'medical', 'ill', 'sickness', 'sick'],
            'icon': '🏥',
            'title': 'Sick Leave'
        },
        'working_hours': {
            'keywords': ['working hours', 'work time', 'schedule', 'shifts', 'office hours', 'hours', 'time', 'work schedule', 'working time'],
            'icon': '⏰',
            'title': 'Working Hours'
        },
        'benefits': {
            'keywords': ['benefits', 'insurance', 'health insurance', 'visa', 'perks', 'benefit', 'health', 'medical insurance'],
            'icon': '🎁',
            'title': 'Employee Benefits'
        },
        'conduct': {
            'keywords': ['conduct', 'behavior', 'dress code', 'professional', 'standards', 'behaviour', 'dress', 'code', 'professional standards'],
            'icon': '👔',
            'title': 'Code of Conduct'
        },
        'disciplinary': {
            'keywords': ['disciplinary', 'warning', 'misconduct', 'punishment', 'violation', 'discipline', 'warnings', 'disciplinary action'],
            'icon': '⚖️',
            'title': 'Disciplinary Procedures'
        },
        'covid': {
            'keywords': ['covid', 'coronavirus', 'quarantine', 'vaccination', 'pandemic', 'covid-19', 'virus', 'vaccine'],
            'icon': '🦠',
            'title': 'COVID-19 Policy'
        },
        'termination': {
            'keywords': ['termination', 'resignation', 'gratuity', 'end of service', 'quit', 'resign', 'leaving', 'end service', 'terminate'],
            'icon': '📋',
            'title': 'Termination & Gratuity'
        },
        # New sub-category mappings
        'health_insurance': {
            'keywords': ['health insurance', 'medical insurance', 'medical coverage', 'health coverage', 'insurance policy'],
            'icon': '🏥',
            'title': 'Health Insurance'
        },
        'visa_sponsorship': {
            'keywords': ['visa sponsorship', 'work visa', 'resident visa', 'visa support', 'immigration'],
            'icon': '📋',
            'title': 'Visa Sponsorship'
        },
        'national_holidays': {
            'keywords': ['national holidays', 'public holidays', 'official holidays', 'eid', 'national day'],
            'icon': '🎆',
            'title': 'National Holidays'
        },
        'administrative_hours': {
            'keywords': ['administrative hours', 'admin hours', 'office hours', 'admin schedule'],
            'icon': '💼',
            'title': 'Administrative Hours'
        },
        'academic_hours': {
            'keywords': ['academic hours', 'teaching hours', 'teaching schedule', 'sessions', 'academic schedule'],
            'icon': '🏫',
            'title': 'Academic Hours'
        },
        'dress_code': {
            'keywords': ['dress code', 'attire', 'clothing', 'appearance', 'professional dress'],
            'icon': '👔',
            'title': 'Dress Code'
        },
        'safeguarding_rules': {
            'keywords': ['safeguarding', 'student safety', 'protection', 'safeguarding rules'],
            'icon': '🛑',
            'title': 'Safeguarding Rules'
        },
        'minor_misconduct': {
            'keywords': ['minor misconduct', 'minor violations', 'lateness', 'attendance issues'],
            'icon': '⚠️',
            'title': 'Minor Misconduct'
        },
        'gross_misconduct': {
            'keywords': ['gross misconduct', 'serious violations', 'theft', 'harassment', 'immediate termination'],
            'icon': '🚨',
            'title': 'Gross Misconduct'
        },
        'performance_appraisal': {
            'keywords': ['performance appraisal', 'performance review', 'annual review', 'evaluation'],
            'icon': '📊',
            'title': 'Performance Appraisal'
        },
        'maternity_leave': {
            'keywords': ['maternity leave', 'maternity', 'pregnancy leave', 'maternity policy'],
            'icon': '🤱',
            'title': 'Maternity Leave'
        },
        'parental_leave': {
            'keywords': ['parental leave', 'paternity leave', 'new parent leave'],
            'icon': '👶',
            'title': 'Parental Leave'
        },
        'bereavement_leave': {
            'keywords': ['bereavement leave', 'bereavement', 'family death', 'funeral leave'],
            'icon': '🕊',
            'title': 'Bereavement Leave'
        }
    }
    
    # Handle specific queries that might be confusing
    special_cases = {
        'interview': 'recruitment',
        'hiring': 'recruitment', 
        'job application': 'recruitment',
        'salary': 'benefits',
        'pay': 'benefits',
        'money': 'benefits',
        'promotion': 'performance',
        'review': 'performance',
        'evaluation': 'performance'
    }
    
    # Check for special cases first
    for special_word, redirect_topic in special_cases.items():
        if special_word in question_lower:
            if redirect_topic == 'recruitment':
                return {
                    'type': 'content',
                    'content': f"""🔍 I understand you're asking about **{special_word}**, but I specialize in providing information about current employee policies from the Alistar Personnel Employee Handbook.

📧 **For recruitment, hiring, and job applications, please contact:**
🏢 **HR Department** at Alistar Personnel
📍 **Location:** 605, Park Avenue , Dubai Silicon Oasis

✨ **I can help current employees with:**
• 🏖️ Annual Leave policies
• ⏰ Working hours and schedules  
• 🎁 Employee benefits
• 👔 Code of conduct
• 📊 Performance management
• And much more!

*Have a great day! I am always here to guide you. Do you want to know more?* 😊"""
                }
            elif redirect_topic == 'benefits':
                data = HANDBOOK_DATA['benefits']
                return {
                    'type': 'content',
                    'content': f"🎁 **{data['title']}**\n\n{data['content']}\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
                }
    
    # Check for ambiguous 'leave' query - show options
    if question_lower in ['leave', 'leaves'] or (len(question_lower.split()) == 1 and 'leave' in question_lower):
        return {
            'type': 'options',
            'content': """🤔 I see you're asking about **leave** policies. There are different types of leave available:

**Please choose which type of leave you'd like to know about:**""",
            'options': [
                {'text': '🏖️ Annual Leave', 'value': 'annual leave', 'description': 'Vacation days, holidays, and time off'},
                {'text': '🏥 Sick Leave', 'value': 'sick leave', 'description': 'Medical leave policies and procedures'},
                {'text': '🤱 Maternity Leave', 'value': 'maternity leave', 'description': 'Maternity leave policies and procedures'},
                {'text': '👶 Parental Leave', 'value': 'parental leave', 'description': 'Parental leave for new parents'},
                {'text': '🕊 Bereavement Leave', 'value': 'bereavement leave', 'description': 'Leave for family bereavement'}
            ],
            'footer': "💡 **Tip:** You can also ask more specifically like 'annual leave' or 'sick leave' for direct answers!\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
        }
    
    # Check for ambiguous 'benefits' query - show options
    if question_lower in ['benefits', 'benefit'] or (len(question_lower.split()) == 1 and any(word in question_lower for word in ['insurance', 'visa', 'perks'])):
        return {
            'type': 'options',
            'content': """🎁 I see you're asking about **employee benefits**. We offer several types of benefits:

**Please choose which benefit you'd like to know about:**""",
            'options': [
                {'text': '🏥 Health Insurance', 'value': 'health insurance', 'description': 'Medical insurance coverage and policies'},
                {'text': '📋 Visa Sponsorship', 'value': 'visa sponsorship', 'description': 'Work visa and dependent visa policies'},
                {'text': '🏖️ Leave Benefits', 'value': 'leave benefits', 'description': 'All types of leave policies'},
                {'text': '🎆 National Holidays', 'value': 'national holidays', 'description': 'Official holidays and public days off'}
            ],
            'footer': "💡 **Tip:** You can also ask specifically about 'health insurance' or 'visa' for direct answers!\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
        }
    
    # Check for ambiguous 'working hours' or 'hours' query - show options
    if question_lower in ['hours', 'working hours', 'schedule', 'shifts'] or (len(question_lower.split()) <= 2 and any(word in question_lower for word in ['working', 'office', 'schedule'])):
        return {
            'type': 'options',
            'content': """⏰ I see you're asking about **working hours**. We have different schedules for different staff:

**Please choose which schedule you'd like to know about:**""",
            'options': [
                {'text': '💼 Administrative Hours', 'value': 'administrative hours', 'description': 'Office hours for administrative staff'},
                {'text': '🏫 Academic Hours', 'value': 'academic hours', 'description': 'Teaching schedule for academic staff'},
                {'text': '🕰️ Overtime Policy', 'value': 'overtime policy', 'description': 'Overtime rules and compensation'},
                {'text': '🌙 Ramadan Hours', 'value': 'ramadan hours', 'description': 'Special working hours during Ramadan'}
            ],
            'footer': "💡 **Tip:** You can also ask specifically about 'admin hours' or 'academic schedule' for direct answers!\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
        }
    
    # Check for ambiguous 'conduct' or 'code' query - show options
    if question_lower in ['conduct', 'code', 'behavior', 'behaviour'] or (len(question_lower.split()) <= 2 and any(word in question_lower for word in ['dress', 'professional', 'standards'])):
        return {
            'type': 'options',
            'content': """👔 I see you're asking about **code of conduct**. There are several important areas:

**Please choose which aspect you'd like to know about:**""",
            'options': [
                {'text': '👔 Dress Code', 'value': 'dress code', 'description': 'Professional attire and appearance standards'},
                {'text': '🛑 Safeguarding Rules', 'value': 'safeguarding rules', 'description': 'Student protection and safety guidelines'},
                {'text': '💼 Professional Standards', 'value': 'professional standards', 'description': 'Employee duties and workplace behavior'},
                {'text': '🤝 Workplace Behavior', 'value': 'workplace behavior', 'description': 'General conduct and interaction guidelines'}
            ],
            'footer': "💡 **Tip:** You can also ask specifically about 'dress code' or 'safeguarding' for direct answers!\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
        }
    
    # Check for ambiguous 'disciplinary' query - show options  
    if question_lower in ['disciplinary', 'discipline', 'warning', 'misconduct'] or (len(question_lower.split()) <= 2 and any(word in question_lower for word in ['punishment', 'violation', 'warnings'])):
        return {
            'type': 'options',
            'content': """⚖️ I see you're asking about **disciplinary procedures**. There are different aspects to understand:

**Please choose which area you'd like to know about:**""",
            'options': [
                {'text': '⚠️ Minor Misconduct', 'value': 'minor misconduct', 'description': 'Examples and consequences of minor violations'},
                {'text': '🚨 Gross Misconduct', 'value': 'gross misconduct', 'description': 'Serious violations and immediate consequences'},
                {'text': '📋 Warning System', 'value': 'warning system', 'description': 'Types of warnings and their validity periods'},
                {'text': '⚖️ Disciplinary Process', 'value': 'disciplinary process', 'description': 'Step-by-step procedure and appeal rights'}
            ],
            'footer': "💡 **Tip:** You can also ask specifically about 'gross misconduct' or 'warnings' for direct answers!\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
        }
    
    # Check for ambiguous 'performance' query - show options
    if question_lower in ['performance', 'review', 'appraisal', 'evaluation'] or (len(question_lower.split()) <= 2 and any(word in question_lower for word in ['probation', 'assessment'])):
        return {
            'type': 'options',
            'content': """📊 I see you're asking about **performance management**. There are key areas to understand:

**Please choose which aspect you'd like to know about:**""",
            'options': [
                {'text': '📊 Performance Appraisal', 'value': 'performance appraisal', 'description': 'Annual review process and procedures'},
                {'text': '⏳ Probation Period', 'value': 'probation period', 'description': 'Probationary period requirements and review'},
                {'text': '📅 Review Schedule', 'value': 'review schedule', 'description': 'When and how often reviews take place'},
                {'text': '📝 Performance Standards', 'value': 'performance standards', 'description': 'Expected standards and evaluation criteria'}
            ],
            'footer': "💡 **Tip:** You can also ask specifically about 'probation' or 'appraisal' for direct answers!\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
        }
    
    # Check for topic matches with scoring
    matches = []
    for topic_key, topic_data in keyword_mappings.items():
        score = 0
        for keyword in topic_data['keywords']:
            if keyword in question_lower:
                if keyword == question_lower:
                    score += 10  # Exact match
                else:
                    score += len(keyword)  # Partial match
        
        if score > 0:
            matches.append((topic_key, score, topic_data))
    
    # Sort matches by score
    matches.sort(key=lambda x: x[1], reverse=True)
    
    # If we found a clear best match
    if matches and matches[0][1] > 0:
        best_match = matches[0][0]
        # Map to HANDBOOK_DATA keys
        handbook_key_mapping = {
            'annual_leave': 'leave',
            'sick_leave': 'sick',
            'working_hours': 'working hours',
            'benefits': 'benefits',
            'conduct': 'conduct',
            'disciplinary': 'disciplinary',
            'covid': 'covid',
            'termination': 'termination',
            # New sub-category mappings
            'health_insurance': 'health insurance',
            'visa_sponsorship': 'visa sponsorship',
            'national_holidays': 'national holidays',
            'administrative_hours': 'administrative hours',
            'academic_hours': 'academic hours',
            'dress_code': 'dress code',
            'safeguarding_rules': 'safeguarding rules',
            'minor_misconduct': 'minor misconduct',
            'gross_misconduct': 'gross misconduct',
            'performance_appraisal': 'performance appraisal',
            'maternity_leave': 'maternity leave',
            'parental_leave': 'parental leave',
            'bereavement_leave': 'bereavement leave'
        }
        
        if best_match in handbook_key_mapping and handbook_key_mapping[best_match] in HANDBOOK_DATA:
            data = HANDBOOK_DATA[handbook_key_mapping[best_match]]
            icon = matches[0][2]['icon']
            return {
                'type': 'content',
                'content': f"{icon} **{data['title']}**\n\n{data['content']}\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
            }
    
    # Check for greeting or general questions
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'thank you', 'thanks']
    if any(greeting in question_lower for greeting in greetings):
        return {
            'type': 'content',
            'content': """👋 Hello! I am your **LGL Employee Helper**. I'm here to help you with any questions about the Alistar Personnel Employee Handbook.

✨ I can assist you with policies, procedures, benefits, and much more. What would you like to know?

*Have a great day! I am always here to guide you. Do you want to know more?* 😊"""
        }
    
    # Default response for unrecognized questions
    return {
        'type': 'options',
        'content': f"🤔 I understand you asked about '{question}', but I couldn't find specific information about that topic in the Employee Handbook.",
        'options': [
            {'text': '🏖️ Annual Leave', 'value': 'annual leave', 'description': 'Vacation days and application process'},
            {'text': '🏥 Sick Leave', 'value': 'sick leave', 'description': 'Medical leave policies and procedures'},
            {'text': '⏰ Working Hours', 'value': 'working hours', 'description': 'Schedule for admin and academic staff'},
            {'text': '🎁 Employee Benefits', 'value': 'benefits', 'description': 'Health insurance, visa, holidays'},
            {'text': '👔 Code of Conduct', 'value': 'conduct', 'description': 'Professional standards and dress code'},
            {'text': '⚖️ Disciplinary Procedures', 'value': 'disciplinary', 'description': 'Warning system and processes'}
        ],
        'footer': "💡 Could you please choose one of these topics or rephrase your question?\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
    }

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 LGL Employee Helper</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">Alistar's Personnel Employee Handbook</p>
</div>
""", unsafe_allow_html=True)

# Employee Login Section
st.sidebar.title("👥 Employee Login")
st.sidebar.markdown("Select your name to access personalized leave information:")

employee_names = ['Select Employee'] + [emp_data['name'] for emp_data in EMPLOYEE_DATA.values()]
selected_employee = st.sidebar.selectbox(
    "Choose your name:",
    employee_names,
    index=0
)

if selected_employee != 'Select Employee':
    # Find employee data
    employee_key = None
    for key, data in EMPLOYEE_DATA.items():
        if data['name'] == selected_employee:
            employee_key = key
            break
    
    if employee_key:
        st.session_state.current_employee = employee_key
        st.session_state.employee_data = EMPLOYEE_DATA[employee_key]
        
        # Show employee info in sidebar
        emp_data = st.session_state.employee_data
        leave_balances = calculate_leave_entitlements(emp_data)
        
        st.sidebar.success(f"Welcome, {emp_data['name']}!")
        st.sidebar.markdown(f"""
        **💼 Employee Details:**
        • Department: {emp_data['department']}
        • Position: {emp_data['position']}
        • Manager: {emp_data['approval_manager']}
        • Service: {emp_data['years_of_service']} years
        
        **📅 Leave Balances:**
        • Annual: {leave_balances['annual_leave']['remaining']} days
        • Sick: {leave_balances['sick_leave']['remaining']} days
        """)
        
        # Form Selection Section
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📝 **Submit a Request Form**")
        st.sidebar.markdown("Select the type of request you'd like to submit:")
        
        # Form type selection
        form_options = ['Select Form Type'] + [f"{form_data['icon']} {form_data['title']}" for form_data in FORM_TYPES.values()]
        selected_form = st.sidebar.selectbox(
            "Request Form:",
            form_options,
            index=0
        )
        
        if selected_form != 'Select Form Type':
            # Extract form type from selection
            form_type_key = None
            for key, form_data in FORM_TYPES.items():
                if f"{form_data['icon']} {form_data['title']}" == selected_form:
                    form_type_key = key
                    break
            
            if form_type_key and st.sidebar.button(f"📝 Submit {FORM_TYPES[form_type_key]['title']}", use_container_width=True):
                st.session_state.show_form = True
                st.session_state.selected_form_type = form_type_key
        
        # Quick leave request button (legacy support)
        st.sidebar.markdown("---")
        if st.sidebar.button("📧 Quick Leave Request", use_container_width=True):
            st.session_state.show_form = True
            st.session_state.selected_form_type = 'leave_request'
            
else:
    st.session_state.current_employee = None
    st.session_state.employee_data = None
    st.sidebar.info("Please select your name to access personalized features like leave balances and request forms.")

# Comprehensive Form System
if 'show_form' in st.session_state and st.session_state.show_form and st.session_state.current_employee:
    form_type = st.session_state.selected_form_type
    form_config = FORM_TYPES[form_type]
    
    st.markdown(f"### {form_config['icon']} {form_config['title']}")
    st.markdown(f"*{form_config['description']}*")
    
    emp_data = st.session_state.employee_data
    
    with st.form(f"{form_type}_form"):
        form_data = {'employee_name': emp_data['name'], 'manager_name': emp_data['approval_manager']}
        
        if form_type == 'leave_request':
            # Leave Request Form
            leave_balances = calculate_leave_entitlements(emp_data)
            
            st.markdown(f"**📅 Your Current Leave Balances:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Annual Leave", f"{leave_balances['annual_leave']['remaining']} days")
            with col2:
                st.metric("Sick Leave", f"{leave_balances['sick_leave']['remaining']} days")
            with col3:
                st.metric("Maternity Leave", f"{leave_balances['maternity_leave']['remaining']} days")
            
            col1, col2 = st.columns(2)
            with col1:
                leave_type = st.selectbox(
                    "Leave Type:",
                    ['Annual Leave', 'Sick Leave', 'Maternity Leave', 'Parental Leave', 'Bereavement Leave']
                )
                start_date = st.date_input("Start Date:", min_value=date.today())
                
            with col2:
                end_date = st.date_input("End Date:", min_value=date.today())
                emergency_contact = st.text_input("Emergency Contact:", placeholder="Name and phone number")
            
            reason = st.text_area("Reason for Leave:", placeholder="Please provide a brief reason for your leave request...")
            
            form_data.update({
                'leave_type': leave_type,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days_requested': (end_date - start_date).days + 1,
                'reason': reason,
                'emergency_contact': emergency_contact
            })
            
        elif form_type == 'visa_request':
            # Visa Request Form
            col1, col2 = st.columns(2)
            with col1:
                visa_type = st.selectbox(
                    "Visa Type:",
                    ['Employee Visa Renewal', 'Dependent Visa Application', 'Visa Cancellation', 'Emirates ID Renewal']
                )
                urgency = st.selectbox("Urgency Level:", ['Normal', 'Urgent', 'Emergency'])
            
            with col2:
                dependent_details = st.text_input("Dependent Details:", placeholder="Names and relationships (if applicable)")
            
            reason = st.text_area("Reason/Additional Information:", placeholder="Please provide details about your visa request...")
            
            form_data.update({
                'visa_type': visa_type,
                'dependent_details': dependent_details,
                'urgency': urgency,
                'reason': reason
            })
            
        elif form_type == 'health_insurance':
            # Health Insurance Form
            col1, col2 = st.columns(2)
            with col1:
                insurance_type = st.selectbox(
                    "Request Type:",
                    ['Add Dependent Coverage', 'Change Provider', 'Upgrade Plan', 'Insurance Claim Support']
                )
                preferred_provider = st.text_input("Preferred Provider:", placeholder="Insurance company preference")
            
            with col2:
                dependent_info = st.text_input("Dependent Information:", placeholder="Names, ages, relationships")
            
            medical_history = st.text_area("Medical History/Special Requirements:", placeholder="Any relevant medical information...")
            
            form_data.update({
                'insurance_type': insurance_type,
                'dependent_info': dependent_info,
                'medical_history': medical_history,
                'preferred_provider': preferred_provider
            })
            
        elif form_type == 'performance_review':
            # Performance Review Form
            col1, col2 = st.columns(2)
            with col1:
                review_type = st.selectbox(
                    "Review Type:",
                    ['Annual Performance Review', 'Mid-Year Review', 'Probation Review', 'Special Assessment']
                )
                preferred_date = st.date_input("Preferred Review Date:", min_value=date.today())
            
            with col2:
                goals = st.text_area("Career Goals:", placeholder="Your professional development goals...")
            
            self_assessment = st.text_area("Self Assessment:", placeholder="Brief summary of your achievements and areas for improvement...")
            
            form_data.update({
                'review_type': review_type,
                'preferred_date': preferred_date.strftime('%Y-%m-%d'),
                'self_assessment': self_assessment,
                'goals': goals
            })
            
        elif form_type == 'training_request':
            # Training Request Form
            col1, col2 = st.columns(2)
            with col1:
                training_type = st.selectbox(
                    "Training Type:",
                    ['Professional Development', 'Technical Training', 'Certification Course', 'Conference/Seminar', 'Online Course']
                )
                course_name = st.text_input("Course/Training Name:", placeholder="Name of the training program")
            
            with col2:
                provider = st.text_input("Training Provider:", placeholder="Institution or company name")
                cost_estimate = st.text_input("Estimated Cost:", placeholder="Total cost (AED)")
            
            justification = st.text_area("Business Justification:", placeholder="How this training will benefit your role and the company...")
            
            form_data.update({
                'training_type': training_type,
                'course_name': course_name,
                'provider': provider,
                'cost_estimate': cost_estimate,
                'justification': justification
            })
            
        elif form_type == 'equipment_request':
            # Equipment Request Form
            col1, col2 = st.columns(2)
            with col1:
                equipment_type = st.selectbox(
                    "Equipment Type:",
                    ['Computer/Laptop', 'Mobile Phone', 'Office Furniture', 'Software License', 'Stationery', 'Other']
                )
                urgency = st.selectbox("Urgency:", ['Normal', 'Urgent', 'Emergency'])
            
            with col2:
                specification = st.text_input("Specifications:", placeholder="Technical requirements or model")
            
            justification = st.text_area("Justification:", placeholder="Why do you need this equipment for your work...")
            
            form_data.update({
                'equipment_type': equipment_type,
                'specification': specification,
                'justification': justification,
                'urgency': urgency
            })
        
        # Submit button
        submitted = st.form_submit_button(f"📧 Submit {form_config['title']}", use_container_width=True)
        
        if submitted:
            # Generate and display email
            subject, html_body = generate_form_email(
                form_config['title'],
                emp_data['name'],
                emp_data['approval_manager'],
                form_data
            )
            
            st.success(f"✅ {form_config['title']} submitted successfully!")
            
            # Display email preview
            st.markdown("### 📧 Email Sent to Manager")
            st.markdown(f"**To:** concessioac@gmail.com")
            st.markdown(f"**Subject:** {subject}")
            
            # Show HTML preview in expander
            with st.expander("🔍 Preview Email Content", expanded=False):
                st.components.v1.html(html_body, height=600, scrolling=True)
            
            # Instructions
            st.markdown("""
            <div style="background: #d4edda; padding: 1rem; border-radius: 10px; border-left: 4px solid #155724; color: #155724;">
                📎 <strong>Next Steps:</strong><br>
                1. Your request has been sent to <strong>concessioac@gmail.com</strong><br>
                2. Your manager will receive an email with approval/rejection buttons<br>
                3. You'll get a response email with the decision<br>
                4. For urgent matters, contact your manager directly
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("Close Form"):
        st.session_state.show_form = False
        st.rerun()

# Legacy leave form support (will be replaced by comprehensive form system)
elif 'show_leave_form' in st.session_state and st.session_state.show_leave_form and st.session_state.current_employee:
    # Redirect to new form system
    st.session_state.show_form = True
    st.session_state.selected_form_type = 'leave_request'
    st.session_state.show_leave_form = False
    st.rerun()

# Quick action buttons with icons
st.markdown("### 🚀 Quick Topics:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏖️ Annual Leave", key="leave_btn", help="Learn about annual leave policies and vacation days"):
        question = 'Tell me about annual leave'
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = process_user_question('annual leave')
        # Handle the new response format
        content = response['content'] if isinstance(response, dict) else response
        st.session_state.messages.append({'role': 'assistant', 'content': content, 'response_data': response})
        st.session_state.processing = False
        st.rerun()
    
    if st.button("🏥 Sick Leave", key="sick_btn", help="Learn about sick leave policies and medical procedures"):
        question = 'Tell me about sick leave'
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = process_user_question('sick leave')
        # Handle the new response format
        content = response['content'] if isinstance(response, dict) else response
        st.session_state.messages.append({'role': 'assistant', 'content': content, 'response_data': response})
        st.session_state.processing = False
        st.rerun()

with col2:
    if st.button("⏰ Working Hours", key="hours_btn", help="Learn about working schedules and time policies"):
        question = 'Tell me about working hours'
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = process_user_question('working hours')
        # Handle the new response format
        content = response['content'] if isinstance(response, dict) else response
        st.session_state.messages.append({'role': 'assistant', 'content': content, 'response_data': response})
        st.session_state.processing = False
        st.rerun()
    
    if st.button("🎁 Benefits", key="benefits_btn", help="Learn about employee benefits and insurance"):
        question = 'Tell me about employee benefits'
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = process_user_question('benefits')
        # Handle the new response format
        content = response['content'] if isinstance(response, dict) else response
        st.session_state.messages.append({'role': 'assistant', 'content': content, 'response_data': response})
        st.session_state.processing = False
        st.rerun()

with col3:
    if st.button("👔 Code of Conduct", key="conduct_btn", help="Learn about professional standards and dress code"):
        question = 'Tell me about code of conduct'
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = process_user_question('conduct')
        # Handle the new response format
        content = response['content'] if isinstance(response, dict) else response
        st.session_state.messages.append({'role': 'assistant', 'content': content, 'response_data': response})
        st.session_state.processing = False
        st.rerun()
    
    if st.button("⚖️ Disciplinary", key="disciplinary_btn", help="Learn about disciplinary procedures and warnings"):
        question = 'Tell me about disciplinary procedures'
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = process_user_question('disciplinary')
        # Handle the new response format
        content = response['content'] if isinstance(response, dict) else response
        st.session_state.messages.append({'role': 'assistant', 'content': content, 'response_data': response})
        st.session_state.processing = False
        st.rerun()

# Employee Data Table Section (for admin/HR view)
st.markdown("---")
if st.checkbox("📈 Show Employee Leave Tracking Data (HR View)"):
    st.markdown("### 📈 Employee Leave Tracking Database")
    
    # Create dataframe for display
    employee_df = []
    for emp_key, emp_data in EMPLOYEE_DATA.items():
        leave_balances = calculate_leave_entitlements(emp_data)
        employee_df.append({
            'Name': emp_data['name'],
            'Employee ID': emp_data['employee_id'],
            'Department': emp_data['department'],
            'Manager': emp_data['approval_manager'],
            'Position': emp_data['position'],
            'Service Years': f"{emp_data['years_of_service']} years",
            'Annual Leave Taken': emp_data['annual_leave_taken'],
            'Annual Leave Remaining': leave_balances['annual_leave']['remaining'],
            'Sick Leave Taken': emp_data['sick_leave_taken'],
            'Sick Leave Remaining': leave_balances['sick_leave']['remaining'],
            'Contract Type': emp_data['contract_type'],
            'Join Date': emp_data['join_date']
        })
    
    df = pd.DataFrame(employee_df)
    
    # Display the table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_employees = len(EMPLOYEE_DATA)
        st.metric("👥 Total Employees", total_employees)
    
    with col2:
        avg_annual_taken = df['Annual Leave Taken'].mean()
        st.metric("🏖️ Avg Annual Leave Taken", f"{avg_annual_taken:.1f} days")
    
    with col3:
        avg_sick_taken = df['Sick Leave Taken'].mean()
        st.metric("🏥 Avg Sick Leave Taken", f"{avg_sick_taken:.1f} days")
    
    with col4:
        departments = df['Department'].nunique()
        st.metric("🏢 Departments", departments)
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="💾 Download Employee Data as CSV",
        data=csv,
        file_name=f"employee_leave_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Chat input using form to prevent auto-rerun
st.markdown("### 💬 Chat with LGL Assistant")

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    if message['role'] == 'assistant':
        # Display the bot message
        st.markdown(f"""
        <div class="bot-message">
            🤖 <strong>LGL Assistant:</strong><br>
            {message['content'].replace('**', '<strong>').replace('**', '</strong>').replace('*', '<em>').replace('*', '</em>').replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Check if this message has options to display
        if 'response_data' in message and isinstance(message['response_data'], dict):
            response_data = message['response_data']
            
            # Handle leave request form
            if response_data.get('type') == 'leave_request':
                emp_data = response_data.get('employee_data')
                leave_balances = response_data.get('leave_balances')
                
                if emp_data and leave_balances:
                    st.markdown("**📧 Quick Leave Request:**")
                    
                    # Quick leave request form
                    with st.form(f"quick_leave_form_{i}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            leave_type = st.selectbox(
                                "Leave Type:",
                                ['Annual Leave', 'Sick Leave', 'Maternity Leave', 'Parental Leave', 'Bereavement Leave'],
                                key=f"leave_type_{i}"
                            )
                            
                            start_date = st.date_input(
                                "Start Date:",
                                min_value=date.today(),
                                key=f"start_date_{i}"
                            )
                            
                        with col2:
                            end_date = st.date_input(
                                "End Date:",
                                min_value=date.today(),
                                key=f"end_date_{i}"
                            )
                            
                            reason = st.text_input(
                                "Reason:",
                                placeholder="Brief reason for leave...",
                                key=f"reason_{i}"
                            )
                        
                        if st.form_submit_button("📧 Generate Email", key=f"submit_{i}"):
                            if start_date and end_date and end_date >= start_date and reason.strip() and emp_data:
                                days_requested = (end_date - start_date).days + 1
                                
                                # Generate email
                                subject, body = generate_form_email(
                                    'Leave Request',
                                    emp_data['name'],
                                    emp_data['approval_manager'],
                                    {
                                        'leave_type': leave_type,
                                        'start_date': start_date.strftime('%Y-%m-%d'),
                                        'end_date': end_date.strftime('%Y-%m-%d'),
                                        'days_requested': days_requested,
                                        'reason': reason,
                                        'employee_name': emp_data['name'],
                                        'manager_name': emp_data['approval_manager']
                                    }
                                )
                                
                                # Add the email to chat
                                email_message = f"""✅ **Leave Request Email Generated!**

**To:** lgldubai@gmail.com
**Subject:** {subject}

**Email Body:**
```
{body}
```

📎 **Next Steps:**
1. Copy the email content above
2. Send it to lgldubai@gmail.com
3. Wait for approval from your manager"""
                                
                                st.session_state.messages.append({
                                    'role': 'assistant',
                                    'content': email_message,
                                    'response_data': {'type': 'content'}
                                })
                                st.rerun()
                
            elif response_data.get('type') == 'options' and 'options' in response_data:
                # Display option buttons
                st.markdown("**Choose an option:**")
                
                # Create columns for buttons
                num_options = len(response_data['options'])
                if num_options <= 2:
                    cols = st.columns(num_options)
                elif num_options <= 4:
                    cols = st.columns(2)
                else:
                    cols = st.columns(3)
                
                for j, option in enumerate(response_data['options']):
                    col_index = j % len(cols)
                    with cols[col_index]:
                        # Create unique key for each button
                        button_key = f"option_{i}_{j}_{option['value'].replace(' ', '_')}"
                        if st.button(
                            option['text'],
                            key=button_key,
                            help=option.get('description', ''),
                            use_container_width=True
                        ):
                            # Add user message for the selected option
                            st.session_state.messages.append({
                                'role': 'user', 
                                'content': f"Tell me about {option['value']}"
                            })
                            
                            # Process the selected option
                            with st.spinner('🔍 Searching through the handbook...'):
                                time.sleep(0.5)
                                response = process_user_question(option['value'])
                                content = response['content'] if isinstance(response, dict) else response
                                st.session_state.messages.append({
                                    'role': 'assistant', 
                                    'content': content,
                                    'response_data': response
                                })
                            
                            st.session_state.processing = False
                            st.rerun()
                
                # Display footer if available
                if 'footer' in response_data and response_data['footer']:
                    st.markdown(f"""
                    <div class="bot-message" style="margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
                        {response_data['footer'].replace('**', '<strong>').replace('**', '</strong>').replace('*', '<em>').replace('*', '</em>').replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")  # Separator after options
    else:
        # User message
        st.markdown(f"""
        <div class="user-message">
            👤 <strong>You:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

# Use form for input to prevent auto-rerun
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("💭 Ask me anything about the Employee Handbook...", 
                               placeholder="e.g., How do I apply for annual leave?",
                               key="chat_input")
    submit_button = st.form_submit_button("🚀 Send")
    
    if submit_button and user_input and user_input.strip():
        # Prevent duplicate processing
        if user_input != st.session_state.last_input and not st.session_state.processing:
            st.session_state.processing = True
            st.session_state.last_input = user_input
            
            # Add user message
            st.session_state.messages.append({'role': 'user', 'content': user_input})
            
            # Process and add assistant response
            with st.spinner('🔍 Searching through the handbook...'):
                time.sleep(1 + random.uniform(0.5, 1.5))  # Simulate processing time
                response = process_user_question(user_input)
                # Handle the new response format
                content = response['content'] if isinstance(response, dict) else response
                st.session_state.messages.append({
                    'role': 'assistant', 
                    'content': content,
                    'response_data': response
                })
            
            st.session_state.processing = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏢 <strong>Alistar Handbook</strong> - Employee Handbook Assistant</p>
    <p>📍 605, Park Avenue , Dubai Silicon Oasis</p>
    <p><em>For additional HR support, please contact the HR Department</em></p>
</div>
""", unsafe_allow_html=True)