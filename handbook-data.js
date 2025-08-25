// Employee Handbook Data - Structured for Intelligent Search
const HANDBOOK_DATA = {
    // Company Information
    company: {
        name: "ES Training DMCC",
        type: "International English language training centre",
        location: "15th Floor, Mazaya Business Avenue, BB1, JLT, Dubai, UAE",
        description: "Teaching English as a foreign language to students from all over the world",
        facilities: "10,000sqft state-of-the-art learning facilities",
        students: "Over 4000 international students from 68 nationalities"
    },

    // Vision, Mission, Goals
    vision: "To create an international EFL and Pathways College that caters for the individual study needs of global students for both short-term camps as well as long-term EFL and Business programmes.",
    
    mission: "To deliver English Language and Business programmes of the highest quality to international students, providing them with the necessary skills to go on to employment and/or further education abroad, and to fulfil their learning objectives in the most efficient and effective manner.",

    // Working Hours
    workingHours: {
        administrative: {
            days: "Monday – Friday",
            hours: "9:00am – 6:00pm",
            overtime: "Paid in accordance to confirmed attendance and at management's discretion"
        },
        academic: {
            days: "Monday to Friday",
            sessions: [
                "9:00am – 12:00pm",
                "12:00pm – 3:00pm", 
                "3:00pm – 6:00pm"
            ],
            minimum: "2 sessions per day",
            flexibility: "Can work overtime conducting third session or decrease to one session during quieter periods"
        },
        ramadan: {
            reduction: "2 hours per day if normal hours exceed 8 hours",
            notice: "1 week notice for revised working times",
            applicable: "Administrative staff only, not teaching staff"
        }
    },

    // Employee Benefits
    benefits: {
        visa: {
            residence: "Company sponsored resident visa",
            dependents: "Available upon request and agreement with line manager",
            costs: "Employee covers all dependent costs including processing fees, visa fees, medical insurance"
        },
        healthInsurance: {
            probation: "Basic Cover (first 6 months)",
            postProbation: "Comprehensive cover (from 6 months)"
        },
        annualLeave: {
            firstYear: "20 working days (after probation completion)",
            subsequentYears: "22 working days from second year onward",
            notice: "Minimum twice the duration of leave requested",
            carryOver: {
                administrative: "Maximum 7 days per year",
                teaching: "Not permitted to carry over"
            },
            calculation: {
                administrative: "20 days first year, 22 days subsequent years",
                teaching: "Pro-rata based on sessions worked: 1 session = 1 day per month, 2/3 sessions = 2 days per month"
            }
        },
        nationalHolidays: [
            "Hijiri's New Year's Day (1 day)",
            "Gregorian's New Year's Day (1 day)", 
            "Eid Al Fitr (2 days)",
            "Eid Al Adha (3 days)",
            "Prophet Mohammed's birthday (1 day)",
            "Isra and Al Miraj (1 day)",
            "National day (1 day)"
        ],
        sickLeave: {
            entitlement: "90 calendar days per year after 3 months post-probation",
            breakdown: {
                fullPay: "First 15 calendar days",
                halfPay: "Next 30 calendar days", 
                noPay: "Next 45 days"
            },
            medicalCertificate: "Required for absence beyond 2 calendar days",
            notification: "1.5 hours for academic staff, 1 hour for admin staff"
        },
        maternity: {
            entitlement: "60 days total",
            breakdown: {
                fullPay: "First 45 consecutive calendar days",
                halfPay: "Following 15 days"
            },
            notice: "15 weeks before due date",
            feedingBreaks: "Two additional breaks of 30 minutes each for 18 months post-delivery",
            extended: "Up to 100 additional consecutive or non-consecutive days without pay"
        },
        parental: {
            female: "5 days within 6 months of birth",
            male: "5 days within 6 months of birth"
        },
        bereavement: {
            spouse: "5 paid days",
            family: "3 paid days for parent, child, sibling, grandchild, or grandparent"
        }
    },

    // Code of Conduct
    conduct: {
        employee_duties: [
            "Ready and willing to work together to create culture of mutual respect",
            "Exercise reasonable skill and care in performing duties",
            "Obey rules, policies, and work directions",
            "Care for company property, equipment, and facilities",
            "Not willfully disrupt business",
            "Hold confidential trade secrets and information",
            "Act in good faith and maintain trust",
            "Maintain healthy work-life balance",
            "Abstain from offensive language, swear words, blaspheme, discriminatory language or sexual innuendos"
        ],
        employer_duties: [
            "Maintain safe working conditions",
            "Protect staff from bullying, harassment, and discrimination", 
            "Provide adequate training and performance feedback",
            "Provide open and transparent communication channels"
        ],
        dressCode: {
            required: "Smart, professional clothes that are clean, tidy, and appropriate",
            prohibited: [
                "Torn, dirty or worn clothing/footwear",
                "Transparent clothing revealing underwear or midriffs",
                "Low-cut necklines",
                "Very short skirts or trousers",
                "Shorts",
                "Flip-flops or beachwear"
            ],
            tattoos: "Should be covered where possible",
            piercings: "Only earrings or nose studs",
            religious: "Appropriate religious and cultural dress permitted unless health/safety risk"
        },
        safeguarding: [
            "No physical contact with students",
            "Avoid being alone with student - keep door open and respectable distance",
            "No personal conversations with students",
            "Maintain clear boundaries",
            "No advice about relationships",
            "No teaching small groups without another staff member present",
            "Be aware of student attachments and keep distance",
            "No contact outside school",
            "No personal contact details to students",
            "No social media following except official ES forums",
            "No private meetings outside school",
            "No vehicle lifts without permission",
            "No private parties or social events",
            "No alcohol when chaperoning",
            "No romantic or sexual relationships with students"
        ]
    },

    // Performance Management
    performance: {
        appraisal: {
            frequency: "Annual formal review after 6-month probation, then yearly",
            midYear: "Optional 6-month verbal review",
            notice: "At least 1 week before meeting",
            confidentiality: "Information shared only with senior management",
            documentation: "Forms provided prior to discussion for preparation"
        },
        probation: {
            duration: "6 months for all new staff",
            extension: "Up to 3 months if appropriate",
            review: "Meeting between employee and line manager at end of period"
        }
    },

    // Disciplinary Procedures
    disciplinary: {
        minor_misconduct: [
            "Persistent lateness and poor timekeeping",
            "Unauthorized absence without valid reason",
            "Abuse of sick leave",
            "Failure to follow prescribed procedures",
            "Private work during working hours",
            "Incompetence",
            "Failure to observe company regulations"
        ],
        gross_misconduct: [
            "Theft, unauthorized possession of company property",
            "Breaches of confidentiality",
            "Being unfit for duty due to drugs/alcohol",
            "Refusal to carry out management instructions",
            "Insulting behaviour/Insubordination",
            "Breach of confidentiality/security",
            "Physical assault, verbal abuse",
            "False declaration of qualifications",
            "Failure to observe safeguarding rules",
            "Willful damage of property",
            "Unlawful discrimination, bullying or harassment",
            "Bringing organization into serious disrepute",
            "Accessing pornographic/offensive material",
            "Bribery/corruption",
            "Intimidation"
        ],
        warnings: {
            verbal: "6 months validity",
            firstWritten: "12 months validity",
            finalWritten: "12 months validity or as agreed"
        },
        process: [
            "Formal investigation by HR",
            "Written charge and hearing notification",
            "Disciplinary hearing with non-biased chairperson",
            "Right to present evidence and call witnesses",
            "Decision communicated in writing",
            "Right to appeal within 5 days"
        ]
    },

    // Termination
    termination: {
        limitedContract: {
            notice: "Generally no notice - expires at end date",
            earlyTermination: {
                employer: "Minimum 3 months' remuneration or remainder if less",
                employee: "Half of 3 months' remuneration or half remainder if less"
            }
        },
        unlimitedContract: {
            notice: "Minimum 30 calendar days",
            summary: "Without notice for gross misconduct per UAE Labour Law Articles 88 and 120"
        },
        gratuity: {
            calculation: [
                "21 calendar days' basic pay for each of first 5 years",
                "30 calendar days' basic pay for each additional year",
                "Maximum total: 2 years' pay"
            ],
            conditions: {
                limited_termination: "Entitled if completed 1+ years",
                limited_resignation: "Not entitled if less than 5 years service",
                unlimited_termination: "Entitled if completed 1+ years", 
                unlimited_resignation: "Sliding scale: 1-3 years (2/3 reduction), 3-5 years (1/3 reduction), 5+ years (no reduction)"
            }
        }
    },

    // COVID-19 Policy
    covid: {
        symptoms: "Immediate isolation and hospital referral",
        testing: "Cannot return until PCR result obtained",
        quarantine: {
            positive: "7 days from 2 days prior to positive test or symptom onset",
            closeContact: "7 days quarantine",
            workFromHome: "Allowed if capable, including online teaching"
        },
        vaccination: "Required proof or weekly PCR tests",
        nonVaccinated: "PCR test every 7 days or annual leave during isolation"
    },

    // Internet and Email Policy
    technology: {
        internet: {
            purpose: "Work purposes only",
            prohibited: [
                "Pornography, obscene, racist, violent, criminal, terrorist content",
                "Gambling and illegal drugs materials",
                "Hacking into unauthorized areas",
                "Downloading commercial software without license",
                "Personal financial gain",
                "Illegal activities",
                "Offensive or harassing material"
            ],
            personal_use: "Limited and reasonable during non-work time only",
            social_media: "Facebook, LinkedIn, YouTube, Twitter, etc. not permitted for personal use"
        },
        email: {
            ownership: "Company emails are official company records",
            prohibited: [
                "Large attachments to many recipients",
                "Content harming company reputation",
                "Offensive, discriminatory, or harassing content",
                "Personal emails from company account",
                "Chain letters or joke emails"
            ],
            security: "Lock terminals when unattended, use caution with unknown attachments"
        }
    }
};

// Keywords mapping for intelligent search
const KEYWORD_MAPPING = {
    // Leave related
    'leave': ['annualLeave', 'sickLeave', 'maternity', 'parental', 'bereavement'],
    'vacation': ['annualLeave'],
    'holiday': ['annualLeave', 'nationalHolidays'],
    'sick': ['sickLeave'],
    'maternity': ['maternity'],
    'parental': ['parental'],
    'bereavement': ['bereavement'],
    'time off': ['annualLeave', 'sickLeave', 'bereavement'],
    
    // Working conditions
    'hours': ['workingHours'],
    'working': ['workingHours', 'conduct'],
    'schedule': ['workingHours'],
    'overtime': ['workingHours'],
    'ramadan': ['workingHours'],
    
    // Benefits
    'benefits': ['benefits'],
    'insurance': ['healthInsurance'],
    'visa': ['visa'],
    'health': ['healthInsurance', 'sickLeave'],
    
    // Conduct and policies
    'conduct': ['conduct'],
    'behavior': ['conduct'],
    'dress': ['conduct'],
    'safeguarding': ['conduct'],
    'disciplinary': ['disciplinary'],
    'misconduct': ['disciplinary'],
    'warning': ['disciplinary'],
    
    // Performance
    'performance': ['performance'],
    'appraisal': ['performance'],
    'review': ['performance'],
    'probation': ['performance'],
    
    // Technology
    'internet': ['technology'],
    'email': ['technology'],
    'computer': ['technology'],
    'social media': ['technology'],
    
    // Termination
    'termination': ['termination'],
    'resignation': ['termination'],
    'notice': ['termination'],
    'gratuity': ['termination'],
    'end of service': ['termination'],
    
    // COVID
    'covid': ['covid'],
    'coronavirus': ['covid'],
    'quarantine': ['covid'],
    'vaccination': ['covid']
};

// Section titles for user-friendly display
const SECTION_TITLES = {
    'workingHours': 'Working Hours',
    'benefits': 'Employee Benefits', 
    'annualLeave': 'Annual Leave',
    'sickLeave': 'Sick Leave',
    'maternity': 'Maternity Leave',
    'parental': 'Parental Leave',
    'bereavement': 'Bereavement Leave',
    'visa': 'Visa & Immigration',
    'healthInsurance': 'Health Insurance',
    'conduct': 'Code of Conduct',
    'performance': 'Performance Management',
    'disciplinary': 'Disciplinary Procedures',
    'termination': 'Termination & End of Service',
    'covid': 'COVID-19 Policy',
    'technology': 'Internet & Email Policy',
    'nationalHolidays': 'National Holidays'
};