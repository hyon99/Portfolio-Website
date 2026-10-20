"""
content.py
All editable site copy and data for the portfolio — name, bio text,
projects, experience, skills, certifications, contact info, and icons.
Edit anything in this file to update what shows up on the site; app.py
only imports these names and renders them.
"""

NAME = "Sudipon Makal"
ROLE_LINE = "Engineering Student • AI Enthusiast • Embedded Systems Developer"
TAGLINE = "More than just a portfolio."
INTRO = (
    "I enjoy turning ideas into intelligent systems—whether that's training "
    "machine learning models, programming microcontrollers, or building "
    "software that solves real-world problems."
)
CURRENT_LINE = (
    "Currently pursuing Electronics and Telecommunication Engineering at "
    "KIIT University, I'm exploring the intersection of Artificial "
    "Intelligence, Embedded Systems, and Enterprise Technology while "
    "continuously expanding my technical skill set."
)
QUOTE = (
    "Learning never stops. Every project, every challenge, and every line "
    "of code is another step toward building meaningful technology."
)
CTA_LINE = "Let's build something impactful together."

EDUCATION = "B.Tech, Electronics & Telecommunication Engineering — KIIT University"
CGPA = "7.88"
GRAD_YEAR = "2027"

ABOUT_PARAGRAPHS = [
    "Technology has always fascinated me—not just because of what it can "
    "do, but because of the problems it can solve.",
    "My journey began with electronics and gradually expanded into "
    "Artificial Intelligence, Deep Learning, Computer Vision, and Embedded "
    "Systems. Today, I enjoy working across both hardware and software, "
    "designing solutions where intelligent algorithms meet real-world "
    "devices.",
    "Beyond academics, I believe growth comes from curiosity, "
    "collaboration, and consistency. Whether it's learning a new "
    "framework, debugging embedded hardware, or understanding enterprise "
    "infrastructure, I enjoy stepping outside my comfort zone.",
    "When I'm not coding or experimenting with new technologies, you'll "
    "probably find me learning something new, earning certifications, or "
    "improving my problem-solving skills.",
]

JOURNEY = [
    ("2023", "The Beginning",
     "Started my B.Tech in Electronics and Telecommunication Engineering "
     "at KIIT University, where I developed a strong foundation in "
     "programming, electronics, and communication systems."),
    ("2024", "Exploring Artificial Intelligence",
     "Discovered my interest in Machine Learning and Deep Learning, "
     "leading me to explore Computer Vision, Neural Networks, and modern "
     "AI technologies through practical implementation and continuous "
     "learning."),
    ("2025", "Embedded Systems",
     "Expanded my knowledge into embedded programming, microcontrollers, "
     "hardware interfacing, and IoT, understanding how intelligent "
     "software can interact with the physical world."),
    ("2026", "Industry Experience",
     "Worked with leading organizations through internships, gaining "
     "practical exposure to both enterprise infrastructure and embedded "
     "system development."),
]

PROJECTS = [
    {
        "title": "Brain Tumor Analysis using MobileNetV3-Large",
        "desc": (
            "Transfer-learning classifier trained on 5,712 MRI images "
            "(1,311 held out for testing) across four tumor classes, using "
            "CLAHE for preprocessing. Test accuracy: 87.63%. Educational "
            "proof-of-concept only — not intended for clinical diagnosis."
        ),
        "tech": ["TensorFlow", "Transfer Learning", "MobileNetV3-Large", "CLAHE"],
        "github": "https://github.com/hyon99/Brain_Tumor_Analysis_MobileNetV3",
    },
    {
        "title": "Smart Wellness System",
        "desc": (
            "Embedded health-monitoring system built on STM32 and ESP32, "
            "reading vitals via MAX30102 and displaying them on an SSD1306 "
            "OLED over UART/I²C."
        ),
        "tech": ["STM32", "ESP32", "MAX30102", "SSD1306 OLED", "UART", "I²C"],
        "github": "https://github.com/hyon99/Smart-Wellness-System",
    },
    {
        "title": "Eye Pointer",
        "desc": (
            "Computer-vision assistive technology that lets a user control "
            "the mouse cursor with eye movement alone."
        ),
        "tech": ["Python", "OpenCV", "MediaPipe", "Computer Vision"],
        "github": "https://github.com/hyon99/EYE-POINTER",
    },
    {
        "title": "Drowsiness Detection",
        "desc": (
            "Real-time CNN-based system that detects driver drowsiness "
            "from webcam video. Approximate accuracy: 98%."
        ),
        "tech": ["TensorFlow", "CNN", "OpenCV"],
        "github": "https://github.com/hyon99/drowsiness_detection",
    },
]

WHAT_I_DO = [
    ("Artificial Intelligence",
     "Building intelligent applications using Machine Learning, Deep "
     "Learning, and Computer Vision to transform data into meaningful "
     "insights."),
    ("Embedded Systems",
     "Developing hardware-integrated solutions using microcontrollers, "
     "sensors, and communication protocols that bridge software with "
     "physical devices."),
    ("Software Development",
     "Creating clean, scalable, and practical applications with a focus "
     "on functionality, reliability, and user experience."),
    ("Continuous Learning",
     "Technology evolves every day—and so do I. I regularly explore new "
     "tools, frameworks, and emerging technologies to stay current and "
     "improve my craft."),
]

EXPERIENCE = [
    {
        "role": "Custom Associate Software Engineer Intern",
        "company": "Accenture",
        "period": "May 2026 – Present",
        "location": "Kolkata, India",
        "summary": (
            "Gaining exposure to enterprise infrastructure support, "
            "working with virtualization technologies, and assisting in "
            "service operations and monitoring — building a practical "
            "understanding of operational reliability at enterprise scale."
        ),
        "gained": [
            "Enterprise Infrastructure Support",
            "Virtualization Technologies",
            "Service Operations & Monitoring",
            "Operational Reliability",
        ],
    },
    {
        "role": "Embedded Systems Intern",
        "company": "Emertxe Information Technologies",
        "period": "December 2025 – January 2026",
        "location": "",
        "summary": (
            "Hands-on work with the PIC16F877A microcontroller — writing "
            "Embedded C, interfacing peripherals, and getting practical "
            "experience developing hardware-driven applications."
        ),
        "gained": [
            "PIC16F877A Programming",
            "Embedded C",
            "Microcontroller Peripherals",
            "Practical Hardware Development",
        ],
    },
    {
        "role": "Student Partner",
        "company": "Internshala",
        "period": "June 2025 – July 2025",
        "location": "",
        "summary": (
            "Led campus marketing and student engagement efforts, "
            "promoting internship opportunities to peers on campus."
        ),
        "gained": [
            "Campus Marketing",
            "Student Engagement",
            "Opportunity Promotion",
        ],
    },
]

SKILLS = {
    "Programming": ["Python", "C", "C++", "Java", "MATLAB", "HTML", "CSS"],
    "AI & Computer Vision": [
        "Machine Learning", "Deep Learning", "TensorFlow", "CNN",
        "Transfer Learning", "OpenCV", "MediaPipe", "Computer Vision",
        "Generative AI", "Prompt Engineering",
    ],
    "Embedded & IoT": [
        "STM32", "ESP32", "PIC16F877A", "MAX30102", "SSD1306 OLED",
        "UART", "I²C", "IoT Development", "Embedded Systems",
    ],
    "Professional": [
        "Communication", "Leadership", "Teamwork",
        "Technical Documentation", "Problem Solving", "Time Management",
    ],
}

CERTIFICATIONS = [
    "Oracle Cloud Infrastructure 2025 Certified Generative AI Professional",
    "Qualcomm AI Upskilling Certificate: Technical Foundation",
    "McKinsey Forward Program",
    "TCS iON Career Edge – IT Primer",
    "TCS iON Career Edge – Young Professional",
    "Infosys Springboard – Prompt Engineering",
    "Infosys Springboard – Computer Vision 101",
    "Machine Learning and DevOps – KIIT",
    "Embedded System Internship – Emertxe",
    "Basic Concepts of Programming with C++",
]
CERTIFICATES_DRIVE_URL = "https://drive.google.com/drive/folders/1hLTc2n3PcVdgPew1z_kByDTctM8nWyLu?usp=drive_link"

GOALS = [
    "Advancing my expertise in Artificial Intelligence",
    "Building scalable software solutions",
    "Exploring intelligent embedded systems",
    "Learning enterprise technologies",
    "Contributing to impactful real-world projects",
]

BEYOND = (
    "While technology is my primary focus, I also value teamwork, "
    "leadership, and community engagement. Through volunteering and "
    "collaborative activities, I've learned that the best solutions "
    "rarely come from working alone. Communication, adaptability, and "
    "empathy are just as important as technical skills."
)

CONTACT = {
    "Email": ("sudiponmakal2004@gmail.com", "mailto:sudiponmakal2004@gmail.com"),
    "Phone": ("+91 9330164939", "tel:+919330164939"),
    "LinkedIn": ("Sudipon Makal", "https://www.linkedin.com/in/sudipon-makal-05067a249/"),
    "GitHub": ("hyon99", "https://github.com/hyon99"),
    "Resume": ("View / Download", "https://drive.google.com/file/d/10huDmBBrlBTaOESTGZQR9pyJg-79JhmW/view?usp=drive_link"),
}

MICROCOPY = {
    "Home": "Turning curiosity into code.",
    "About Me": "Every expert was once a beginner.",
    "Experience": "Engineering ideas into reality.",
    "Projects": "Building intelligent systems, one challenge at a time.",
    "Contact Me": "Driven by curiosity. Guided by purpose.",
    "AI Agent": "Ask, and the code shall answer.",
}

ICONS = {
    "Email": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6.5h18v11H3z"/><path d="M3 6.5l9 7 9-7"/></svg>',
    "Phone": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6.5 3.5c-1.5 0-2.5 1-2.5 2.5 0 7.5 6.5 14 14 14 1.5 0 2.5-1 2.5-2.5v-2l-4-1.5-1.5 1.5c-2-1-4-3-5-5l1.5-1.5-1.5-4z"/></svg>',
    "LinkedIn": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M7.5 10v7M7.5 7.2v.2M11.5 17v-4.2c0-1.4 1-2.3 2.3-2.3 1.3 0 2.2.9 2.2 2.3V17"/></svg>',
    "GitHub": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 19c-4 1.2-4-2-6-2m12 4v-3.2c0-.9.3-1.5.8-2-2.6-.3-5.3-1.3-5.3-5.6 0-1.2.4-2.2 1.2-3-.2-.3-.5-1.6.1-3.2 0 0 1-.3 3.2 1.2a11 11 0 016 0c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.3 2.9.1 3.2.8.8 1.2 1.8 1.2 3 0 4.3-2.7 5.3-5.3 5.6.5.5.9 1.3.9 2.6V19"/></svg>',
    "Resume": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M7 3.5h7l4 4V20a1 1 0 01-1 1H7a1 1 0 01-1-1V4.5a1 1 0 011-1z"/><path d="M14 3.5V8h4M9 12.5h6M9 15.8h6M9 9.3h2.5"/></svg>',
}
