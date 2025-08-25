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
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
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
    }
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        'role': 'assistant',
        'content': '👋 Hello! I am your **LGL Employee Helper**. Ask me anything about the ES Training DMCC Employee Handbook!\n\nI can help you with policies, procedures, benefits, and much more. What would you like to know?'
    })

def process_user_question(question):
    """Process user question and return appropriate response"""
    question_lower = question.lower()
    
    # Check for topic matches
    for topic, data in HANDBOOK_DATA.items():
        if topic in question_lower or any(keyword in question_lower for keyword in [
            'annual leave' if topic == 'leave' else topic,
            'vacation' if topic == 'leave' else '',
            'holiday' if topic == 'leave' else '',
            'illness' if topic == 'sick' else '',
            'medical' if topic == 'sick' else '',
            'schedule' if topic == 'working hours' else '',
            'time' if topic == 'working hours' else '',
            'insurance' if topic == 'benefits' else '',
            'visa' if topic == 'benefits' else '',
            'dress' if topic == 'conduct' else '',
            'behavior' if topic == 'conduct' else '',
            'warning' if topic == 'disciplinary' else '',
            'misconduct' if topic == 'disciplinary' else '',
            'coronavirus' if topic == 'covid' else '',
            'quarantine' if topic == 'covid' else '',
            'resignation' if topic == 'termination' else '',
            'gratuity' if topic == 'termination' else ''
        ]):
            return f"📖 **{data['title']}**\n\n{data['content']}\n\n*Have a great day! I am always here to guide you. Do you want to know more?* 😊"
    
    # Default response for unrecognized questions
    return """I understand you're looking for information from the Employee Handbook. I can help you with:

🔹 **Annual Leave** - Vacation days and application process
🔹 **Sick Leave** - Medical leave policies and procedures  
🔹 **Working Hours** - Schedule for admin and academic staff
🔹 **Employee Benefits** - Health insurance, visa, holidays
🔹 **Code of Conduct** - Professional standards and dress code
🔹 **Disciplinary Procedures** - Warning system and processes
🔹 **COVID-19 Policy** - Health and safety protocols
🔹 **Termination & Gratuity** - End of service procedures

Please ask about any of these topics, and I'll provide detailed information!

*Have a great day! I am always here to guide you. Do you want to know more?* 😊"""

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 LGL Employee Helper</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">Your intelligent guide to the ES Training DMCC Employee Handbook</p>
</div>
""", unsafe_allow_html=True)

# Quick action buttons
st.markdown("### 🚀 Quick Topics:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📅 Annual Leave", key="leave_btn"):
        st.session_state.messages.append({'role': 'user', 'content': 'Tell me about annual leave'})
        response = process_user_question('annual leave')
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    if st.button("🏥 Sick Leave", key="sick_btn"):
        st.session_state.messages.append({'role': 'user', 'content': 'Tell me about sick leave'})
        response = process_user_question('sick leave')
        st.session_state.messages.append({'role': 'assistant', 'content': response})

with col2:
    if st.button("⏰ Working Hours", key="hours_btn"):
        st.session_state.messages.append({'role': 'user', 'content': 'Tell me about working hours'})
        response = process_user_question('working hours')
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    if st.button("🎁 Benefits", key="benefits_btn"):
        st.session_state.messages.append({'role': 'user', 'content': 'Tell me about employee benefits'})
        response = process_user_question('benefits')
        st.session_state.messages.append({'role': 'assistant', 'content': response})

with col3:
    if st.button("👔 Code of Conduct", key="conduct_btn"):
        st.session_state.messages.append({'role': 'user', 'content': 'Tell me about code of conduct'})
        response = process_user_question('conduct')
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    if st.button("⚖️ Disciplinary", key="disciplinary_btn"):
        st.session_state.messages.append({'role': 'user', 'content': 'Tell me about disciplinary procedures'})
        response = process_user_question('disciplinary')
        st.session_state.messages.append({'role': 'assistant', 'content': response})

# Chat interface
st.markdown("### 💬 Chat with LGL Assistant")

# Display chat messages
for message in st.session_state.messages:
    if message['role'] == 'assistant':
        st.markdown(f"""
        <div class="bot-message">
            🤖 <strong>LGL Assistant:</strong><br>
            {message['content'].replace('**', '<strong>').replace('**', '</strong>').replace('*', '<em>').replace('*', '</em>').replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="user-message">
            👤 <strong>You:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input("💭 Ask me anything about the Employee Handbook...", key="user_input", placeholder="e.g., How do I apply for annual leave?")

if user_input:
    # Add user message
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    # Process and add assistant response
    with st.spinner('🔍 Searching through the handbook...'):
        time.sleep(1 + random.uniform(0.5, 1.5))  # Simulate processing time
        response = process_user_question(user_input)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    # Rerun to update the display
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏢 <strong>ES Training DMCC</strong> - Employee Handbook Assistant</p>
    <p>📍 15th Floor, Mazaya Business Avenue, BB1, JLT, Dubai, UAE</p>
    <p><em>For additional HR support, please contact the HR Department</em></p>
</div>
""", unsafe_allow_html=True)