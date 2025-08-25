# 🤖 LGL Employee Helper

An intelligent AI-powered chatbot that provides comprehensive assistance for ES Training DMCC Employee Handbook queries.

## 🌟 Features

### 🎯 **Intelligent Question Answering**
- Natural language processing for employee handbook queries
- Smart keyword detection and topic mapping
- Context-aware responses with relevant information
- Comprehensive coverage of all handbook sections

### 💬 **Interactive Interface**
- Modern, responsive design with professional styling
- Real-time chat interface
- Quick action buttons for common topics
- Beautiful gradient backgrounds and smooth animations

### 📚 **Complete Handbook Coverage**
- **Working Hours** (Administrative & Academic staff)
- **Employee Benefits** (Health insurance, Visa sponsorship)
- **Leave Policies** (Annual, Sick, Maternity, Parental, Bereavement)
- **Code of Conduct** (Professional standards, Dress code, Safeguarding)
- **Performance Management** (Appraisals, Probation)
- **Disciplinary Procedures** (Misconduct, Warnings, Appeals)
- **COVID-19 Policy** (Health protocols, Quarantine rules)
- **Termination & Gratuity** (Notice periods, End of service benefits)

## 🚀 Live Demo

### Streamlit Cloud Deployment
1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Sign in** with your GitHub account
4. **Click "New app"**
5. **Select your forked repository**
6. **Set main file path** to: `app.py`
7. **Click "Deploy"**

### Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/lgl-employee-helper.git
cd lgl-employee-helper

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## 📁 File Structure

```
lgl-employee-helper/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── index.html         # Alternative HTML version
├── styles.css         # CSS styling (for HTML version)
├── script.js          # JavaScript logic (for HTML version)
├── handbook-data.js   # Structured handbook data (for HTML version)
└── server.py          # Simple Python server (for HTML version)
```

## 💻 Two Deployment Options

### Option 1: Streamlit App (Recommended)
- **File:** `app.py`
- **Features:** Interactive web app with Python backend
- **Deployment:** Streamlit Cloud, Heroku, or any Python hosting
- **Benefits:** Easy deployment, automatic scaling, built-in analytics

### Option 2: Static HTML App
- **File:** `index.html`
- **Features:** Self-contained HTML with embedded CSS/JS
- **Deployment:** GitHub Pages, Netlify, Vercel, or any static hosting
- **Benefits:** No server required, fast loading, works offline

## 🛠️ Technical Details

### Streamlit App Features
- **Modern UI:** Custom CSS with gradient backgrounds and animations
- **Chat Interface:** Real-time messaging with bot responses
- **Quick Actions:** Pre-defined buttons for common queries
- **Smart Processing:** Keyword-based topic detection and response generation
- **Session Management:** Maintains conversation history during session

### Data Structure
All employee handbook information is structured and organized for quick retrieval:
- Comprehensive policy details
- Step-by-step procedures
- Reference sections
- Contact information

## 📋 Example Queries

Try asking the bot these questions:

### **Leave & Time Off**
- "How do I apply for annual leave?"
- "How many sick days do I get?"
- "What is the maternity leave policy?"
- "When are the national holidays?"

### **Working Conditions**
- "What are the working hours?"
- "Can I work overtime?"
- "What happens during Ramadan?"

### **Benefits & Policies**
- "What benefits do I get?"
- "How does health insurance work?"
- "What is the dress code?"
- "Tell me about the code of conduct"

### **Performance & Discipline**
- "How does the appraisal process work?"
- "What is the probation period?"
- "What happens if I get a warning?"

## 🎨 Customization

### Branding
- Update company name and logo in `app.py`
- Modify color scheme in the CSS section
- Add custom company information

### Content
- Edit handbook data in the `HANDBOOK_DATA` dictionary
- Add new topics and sections
- Update policy information as needed

### Styling
- Customize CSS in the `st.markdown()` sections
- Modify button styles and colors
- Adjust layout and spacing

## 🔧 Development

### Adding New Topics
1. Add new entry to `HANDBOOK_DATA` dictionary
2. Include topic keywords in the processing function
3. Test with relevant queries

### Enhancing Responses
1. Improve keyword detection logic
2. Add more sophisticated NLP processing
3. Include context awareness for follow-up questions

## 📱 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Create an issue in this repository
- Contact the HR Department at ES Training DMCC
- Email: [your-email@company.com]

## 🏢 About ES Training DMCC

ES Training is an international English language training centre based in Dubai, UAE. We provide high-quality English language education to students from around the world.

**Location:** 15th Floor, Mazaya Business Avenue, BB1, JLT, Dubai, UAE

---

**Built with ❤️ for ES Training DMCC employees**