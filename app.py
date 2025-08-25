import streamlit as st
import re
import time
import random

# Configure the page
st.set_page_config(
    page_title="LGL Employee Helper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
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

# Initialize input tracking to prevent loops
if 'last_input' not in st.session_state:
    st.session_state.last_input = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False

def process_user_question(question):
    """Process user question and return appropriate response"""
    question_lower = question.lower().strip()
    
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
            if response_data.get('type') == 'options' and 'options' in response_data:
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