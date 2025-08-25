// LGL Employee Helper - Advanced AI Chatbot
class EmployeeHelper {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendButton');
        this.loading = document.getElementById('loading');
        this.quickActions = document.getElementById('quickActions');
        this.inputSuggestions = document.getElementById('inputSuggestions');
        
        this.conversationContext = [];
        this.currentTopic = null;
        this.userPreferences = {};
        
        this.initializeEventListeners();
        this.showWelcomeMessage();
    }

    initializeEventListeners() {
        // Enter key to send message
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Input suggestions
        this.chatInput.addEventListener('input', (e) => {
            this.showInputSuggestions(e.target.value);
        });

        // Send button click
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
    }

    showWelcomeMessage() {
        // Hide quick actions after welcome
        setTimeout(() => {
            this.quickActions.style.display = 'none';
        }, 3000);
    }

    showInputSuggestions(input) {
        if (input.length < 2) {
            this.inputSuggestions.innerHTML = '';
            return;
        }

        const suggestions = this.generateSuggestions(input);
        if (suggestions.length > 0) {
            this.inputSuggestions.innerHTML = suggestions
                .map(suggestion => `<span class="suggestion-chip" onclick="employeeHelper.applySuggestion('${suggestion}')">${suggestion}</span>`)
                .join('');
        } else {
            this.inputSuggestions.innerHTML = '';
        }
    }

    generateSuggestions(input) {
        const lowercaseInput = input.toLowerCase();
        const suggestions = [];

        // Common question starters
        if (lowercaseInput.includes('how')) {
            suggestions.push('How do I apply for annual leave?', 'How many sick days do I get?', 'How does the probation period work?');
        }
        if (lowercaseInput.includes('what')) {
            suggestions.push('What are the working hours?', 'What benefits do I get?', 'What is the dress code?');
        }
        if (lowercaseInput.includes('when')) {
            suggestions.push('When can I take leave?', 'When do I get health insurance?', 'When is the appraisal?');
        }

        // Topic-based suggestions
        Object.keys(KEYWORD_MAPPING).forEach(keyword => {
            if (lowercaseInput.includes(keyword)) {
                const topics = KEYWORD_MAPPING[keyword];
                topics.forEach(topic => {
                    if (SECTION_TITLES[topic]) {
                        suggestions.push(`Tell me about ${SECTION_TITLES[topic]}`);
                    }
                });
            }
        });

        return [...new Set(suggestions)].slice(0, 3);
    }

    applySuggestion(suggestion) {
        this.chatInput.value = suggestion;
        this.inputSuggestions.innerHTML = '';
        this.sendMessage();
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // Clear input and suggestions
        this.chatInput.value = '';
        this.inputSuggestions.innerHTML = '';
        
        // Hide quick actions
        this.quickActions.style.display = 'none';

        // Add user message
        this.addMessage(message, 'user');
        
        // Show loading
        this.showLoading();
        
        // Process message and get response
        setTimeout(() => {
            const response = this.processMessage(message);
            this.hideLoading();
            this.addMessage(response.text, 'bot', response.options, response.followUp);
            
            // Update conversation context
            this.conversationContext.push({
                user: message,
                bot: response.text,
                topic: response.topic,
                timestamp: new Date()
            });
        }, 1000 + Math.random() * 1000); // Simulate processing time
    }

    processMessage(message) {
        const lowercaseMessage = message.toLowerCase();
        
        // Detect intent and extract keywords
        const intent = this.detectIntent(lowercaseMessage);
        const keywords = this.extractKeywords(lowercaseMessage);
        const topics = this.findRelevantTopics(keywords);
        
        // Generate response based on intent and topics
        return this.generateResponse(intent, topics, keywords, message);
    }

    detectIntent(message) {
        // Question words
        if (message.includes('how')) return 'how';
        if (message.includes('what')) return 'what';
        if (message.includes('when')) return 'when';
        if (message.includes('where')) return 'where';
        if (message.includes('why')) return 'why';
        if (message.includes('who')) return 'who';
        
        // Action words
        if (message.includes('apply') || message.includes('request')) return 'apply';
        if (message.includes('calculate') || message.includes('compute')) return 'calculate';
        if (message.includes('explain') || message.includes('tell')) return 'explain';
        
        return 'general';
    }

    extractKeywords(message) {
        const keywords = [];
        Object.keys(KEYWORD_MAPPING).forEach(keyword => {
            if (message.includes(keyword)) {
                keywords.push(keyword);
            }
        });
        return keywords;
    }

    findRelevantTopics(keywords) {
        const topics = new Set();
        keywords.forEach(keyword => {
            if (KEYWORD_MAPPING[keyword]) {
                KEYWORD_MAPPING[keyword].forEach(topic => topics.add(topic));
            }
        });
        return Array.from(topics);
    }

    generateResponse(intent, topics, keywords, originalMessage) {
        if (topics.length === 0) {
            return this.generateGeneralResponse(originalMessage);
        }

        if (topics.length === 1) {
            return this.generateTopicResponse(topics[0], intent, keywords);
        }

        // Multiple topics - offer options
        return this.generateMultiTopicResponse(topics, keywords);
    }

    generateGeneralResponse(message) {
        const responses = [
            "I understand you're looking for information from the Employee Handbook. Could you be more specific about what topic you'd like to know about?",
            "I'm here to help with any questions about ES Training DMCC policies and procedures. What specific area would you like me to explain?",
            "Let me help you find the right information in the Employee Handbook. Could you tell me which topic interests you most?"
        ];

        const commonTopics = ['Working Hours', 'Annual Leave', 'Employee Benefits', 'Code of Conduct', 'Sick Leave', 'Performance Management'];
        
        return {
            text: responses[Math.floor(Math.random() * responses.length)],
            options: commonTopics,
            followUp: "Here are some common topics I can help with:",
            topic: 'general'
        };
    }

    generateTopicResponse(topic, intent, keywords) {
        const data = this.getTopicData(topic);
        let response = '';
        let options = [];
        let followUp = '';

        switch (topic) {
            case 'workingHours':
                response = this.formatWorkingHoursResponse(data, intent);
                options = ['Administrative Hours', 'Academic Hours', 'Overtime Policy', 'Ramadan Hours'];
                break;
            
            case 'annualLeave':
                response = this.formatAnnualLeaveResponse(data, intent);
                options = ['Leave Entitlement', 'How to Apply', 'Carry Over Rules', 'Peak Periods'];
                break;
            
            case 'sickLeave':
                response = this.formatSickLeaveResponse(data, intent);
                options = ['Entitlement Details', 'How to Apply', 'Medical Certificate', 'Sick Leave Types'];
                break;
                
            case 'benefits':
                response = this.formatBenefitsResponse(data, intent);
                options = ['Health Insurance', 'Visa Sponsorship', 'Leave Policies', 'National Holidays'];
                break;
                
            case 'conduct':
                response = this.formatConductResponse(data, intent);
                options = ['Employee Duties', 'Dress Code', 'Safeguarding', 'Professional Standards'];
                break;
                
            case 'disciplinary':
                response = this.formatDisciplinaryResponse(data, intent);
                options = ['Minor Misconduct', 'Gross Misconduct', 'Warning System', 'Appeal Process'];
                break;
                
            default:
                response = this.formatGeneralTopicResponse(topic, data);
                break;
        }

        followUp = "Would you like to know more about any of these specific areas?";

        return {
            text: response,
            options: options,
            followUp: followUp,
            topic: topic
        };
    }

    generateMultiTopicResponse(topics, keywords) {
        const topicTitles = topics.map(topic => SECTION_TITLES[topic] || topic);
        
        const response = `I found information related to multiple topics in the Employee Handbook. Which area would you like me to focus on?`;
        
        return {
            text: response,
            options: topicTitles,
            followUp: "Please select the topic you're most interested in:",
            topic: 'multiple'
        };
    }

    formatWorkingHoursResponse(data, intent) {
        let response = "📅 **Working Hours at ES Training DMCC:**\n\n";
        
        response += "**Administrative Staff:**\n";
        response += `• Days: ${data.administrative.days}\n`;
        response += `• Hours: ${data.administrative.hours}\n\n`;
        
        response += "**Academic Staff:**\n";
        response += `• Days: ${data.academic.days}\n`;
        response += `• Sessions: ${data.academic.sessions.join(', ')}\n`;
        response += `• Minimum: ${data.academic.minimum}\n`;
        response += `• Note: ${data.academic.flexibility}\n\n`;
        
        if (intent === 'how') {
            response += "💡 **How it works:** Academic staff have flexible scheduling and can work additional sessions based on demand.\n\n";
        }
        
        response += `⏰ **Ramadan Hours:** ${data.ramadan.reduction} (${data.ramadan.applicable})`;
        
        return response;
    }

    formatAnnualLeaveResponse(data, intent) {
        let response = "🏖️ **Annual Leave Policy:**\n\n";
        
        response += "**Entitlement:**\n";
        response += `• First Year: ${data.firstYear}\n`;
        response += `• Subsequent Years: ${data.subsequentYears}\n\n`;
        
        if (intent === 'how') {
            response += "**How to Apply:**\n";
            response += `• Submit request with ${data.notice}\n`;
            response += "• Use Annual Leave Form\n";
            response += "• Submit to Line Manager\n";
            response += "• First-come, first-served basis\n\n";
        }
        
        response += "**Carry Over Rules:**\n";
        response += `• Administrative Staff: ${data.carryOver.administrative}\n`;
        response += `• Teaching Staff: ${data.carryOver.teaching}\n\n`;
        
        response += "📋 **Reference:** Section 9.2 of Employee Handbook";
        
        return response;
    }

    formatSickLeaveResponse(data, intent) {
        let response = "🏥 **Sick Leave Policy:**\n\n";
        
        response += "**Entitlement (per year):**\n";
        response += `• Full Pay: ${data.breakdown.fullPay}\n`;
        response += `• Half Pay: ${data.breakdown.halfPay}\n`;
        response += `• No Pay: ${data.breakdown.noPay}\n\n`;
        
        if (intent === 'how') {
            response += "**How to Apply:**\n";
            response += `• Notify manager within ${data.notification}\n`;
            response += "• Complete Sick Leave Form upon return\n";
            response += `• Medical certificate required if absence exceeds ${data.medicalCertificate.split(' ')[0]} days\n\n`;
        }
        
        response += "⚠️ **Important:** Available after completing 3 months post-probation period.\n\n";
        response += "📋 **Reference:** Section 9.3 of Employee Handbook";
        
        return response;
    }

    formatBenefitsResponse(data, intent) {
        let response = "🎁 **Employee Benefits Overview:**\n\n";
        
        response += "**Health Insurance:**\n";
        response += `• Probation Period: ${data.healthInsurance.probation}\n`;
        response += `• After 6 Months: ${data.healthInsurance.postProbation}\n\n`;
        
        response += "**Visa Sponsorship:**\n";
        response += `• ${data.visa.residence}\n`;
        response += `• Dependents: ${data.visa.dependents}\n\n`;
        
        response += "**Leave Benefits:**\n";
        response += `• Annual Leave: ${data.annualLeave.firstYear} → ${data.annualLeave.subsequentYears}\n`;
        response += `• Sick Leave: ${data.sickLeave.entitlement}\n`;
        response += `• Maternity: ${data.maternity.entitlement}\n`;
        response += `• Parental: ${data.parental.female} (female), ${data.parental.male} (male)\n\n`;
        
        response += "📋 **Reference:** Section 9 of Employee Handbook";
        
        return response;
    }

    formatConductResponse(data, intent) {
        let response = "👔 **Code of Conduct:**\n\n";
        
        response += "**Professional Standards:**\n";
        response += "• Create culture of mutual respect\n";
        response += "• Exercise reasonable skill and care\n";
        response += "• Maintain confidentiality\n";
        response += "• Professional language at all times\n\n";
        
        response += "**Dress Code:**\n";
        response += `• Required: ${data.dressCode.required}\n`;
        response += "• Prohibited: Torn/dirty clothing, inappropriate wear, flip-flops\n";
        response += `• Tattoos: ${data.dressCode.tattoos}\n\n`;
        
        if (keywords.includes('safeguarding') || intent === 'safeguarding') {
            response += "**Student Safeguarding:**\n";
            response += "• No physical contact with students\n";
            response += "• Avoid being alone with students\n";
            response += "• Maintain professional boundaries\n";
            response += "• No personal relationships\n\n";
        }
        
        response += "📋 **Reference:** Section 6 of Employee Handbook";
        
        return response;
    }

    formatDisciplinaryResponse(data, intent) {
        let response = "⚖️ **Disciplinary Procedures:**\n\n";
        
        response += "**Warning System:**\n";
        response += `• Verbal Warning: ${data.warnings.verbal} validity\n`;
        response += `• First Written: ${data.warnings.firstWritten} validity\n`;
        response += `• Final Written: ${data.warnings.finalWritten} validity\n\n`;
        
        response += "**Minor Misconduct Examples:**\n";
        response += "• Persistent lateness\n";
        response += "• Unauthorized absence\n";
        response += "• Failure to follow procedures\n\n";
        
        response += "**Gross Misconduct Examples:**\n";
        response += "• Theft of company property\n";
        response += "• Breach of confidentiality\n";
        response += "• Being unfit for duty\n";
        response += "• Safeguarding violations\n\n";
        
        if (intent === 'how') {
            response += "**Process:**\n";
            response += "1. Formal investigation\n";
            response += "2. Written notification\n";
            response += "3. Disciplinary hearing\n";
            response += "4. Decision & communication\n";
            response += "5. Right to appeal (within 5 days)\n\n";
        }
        
        response += "📋 **Reference:** Section 12 of Employee Handbook";
        
        return response;
    }

    formatGeneralTopicResponse(topic, data) {
        const title = SECTION_TITLES[topic] || topic;
        return `📖 **${title}:**\n\nI have detailed information about this topic in the Employee Handbook. Could you please be more specific about what aspect you'd like to know about?`;
    }

    getTopicData(topic) {
        switch (topic) {
            case 'workingHours': return HANDBOOK_DATA.workingHours;
            case 'annualLeave': return HANDBOOK_DATA.benefits.annualLeave;
            case 'sickLeave': return HANDBOOK_DATA.benefits.sickLeave;
            case 'benefits': return HANDBOOK_DATA.benefits;
            case 'conduct': return HANDBOOK_DATA.conduct;
            case 'disciplinary': return HANDBOOK_DATA.disciplinary;
            case 'maternity': return HANDBOOK_DATA.benefits.maternity;
            case 'parental': return HANDBOOK_DATA.benefits.parental;
            case 'performance': return HANDBOOK_DATA.performance;
            case 'termination': return HANDBOOK_DATA.termination;
            case 'covid': return HANDBOOK_DATA.covid;
            case 'technology': return HANDBOOK_DATA.technology;
            default: return {};
        }
    }

    addMessage(content, sender, options = [], followUp = '') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Format content with markdown-like styling
        let formattedContent = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
        
        contentDiv.innerHTML = formattedContent;
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        // Add options if provided
        if (options.length > 0 && sender === 'bot') {
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'option-buttons';
            
            if (followUp) {
                const followUpP = document.createElement('p');
                followUpP.innerHTML = followUp;
                followUpP.style.marginTop = '10px';
                followUpP.style.marginBottom = '10px';
                followUpP.style.fontSize = '0.9rem';
                followUpP.style.color = '#666';
                contentDiv.appendChild(followUpP);
            }
            
            options.forEach(option => {
                const button = document.createElement('button');
                button.className = 'option-btn';
                button.textContent = option;
                button.onclick = () => this.handleOptionClick(option);
                optionsDiv.appendChild(button);
            });
            
            contentDiv.appendChild(optionsDiv);
        }
        
        // Add follow-up message for bot
        if (sender === 'bot') {
            const followUpDiv = document.createElement('div');
            followUpDiv.className = 'bot-followup';
            followUpDiv.innerHTML = '<br><em>Have a great day! I am always here to guide you. Do you want to know more? 😊</em>';
            contentDiv.appendChild(followUpDiv);
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    handleOptionClick(option) {
        // Simulate user clicking on an option
        this.addMessage(option, 'user');
        
        // Process the option as a new message
        setTimeout(() => {
            const response = this.processMessage(option);
            this.addMessage(response.text, 'bot', response.options, response.followUp);
        }, 500);
    }

    showLoading() {
        this.loading.style.display = 'flex';
    }

    hideLoading() {
        this.loading.style.display = 'none';
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Quick action handlers
function handleQuickAction(topic) {
    employeeHelper.addMessage(`Tell me about ${topic}`, 'user');
    
    setTimeout(() => {
        const response = employeeHelper.processMessage(topic);
        employeeHelper.addMessage(response.text, 'bot', response.options, response.followUp);
    }, 500);
}

// Send message function (for HTML onclick)
function sendMessage() {
    employeeHelper.sendMessage();
}

// Initialize the application
let employeeHelper;
document.addEventListener('DOMContentLoaded', () => {
    employeeHelper = new EmployeeHelper();
});

// Advanced Features
class AdvancedFeatures {
    static generateContextualSuggestions(conversationHistory) {
        // Analyze conversation to suggest related topics
        const suggestions = [];
        
        if (conversationHistory.some(msg => msg.topic === 'annualLeave')) {
            suggestions.push('National Holidays', 'Sick Leave Policy');
        }
        
        if (conversationHistory.some(msg => msg.topic === 'disciplinary')) {
            suggestions.push('Code of Conduct', 'Performance Management');
        }
        
        return suggestions;
    }
    
    static detectFollowUpQuestions(message) {
        const followUpPatterns = [
            'what about',
            'how about',
            'what if',
            'can i also',
            'and what',
            'tell me more'
        ];
        
        return followUpPatterns.some(pattern => 
            message.toLowerCase().includes(pattern)
        );
    }
    
    static calculateLeaveEntitlement(serviceYears, employeeType) {
        if (employeeType === 'administrative') {
            return serviceYears >= 1 ? 22 : 20;
        } else if (employeeType === 'academic') {
            // Pro-rata calculation for academic staff
            return 'Calculated based on sessions worked';
        }
        return 0;
    }
}