# Career Manager Streamlit 💼

A streamlined Streamlit application to organize and manage job applications in one centralized place. Track your applications, monitor job search activities, and visualize your career management progress with an intuitive dashboard.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?style=flat-square&logo=pandas&logoColor=white)
![Altair](https://img.shields.io/badge/Altair-5.5.0-0078AA?style=flat-square&logo=altair&logoColor=white)

**Core Technologies:**
- **Python** – Application programming language
- **Streamlit** – Interactive web framework for data applications
- **Pandas** – Data manipulation and analysis
- **Altair** – Declarative visualization library
- **JSON** – Data storage and management

---

## 📂 Project Structure

```
career-manager-streamlit/
├── main.py                 # Entry point with navigation and authentication
├── pages/                  # Streamlit multi-page application
│   ├── dashboard.py       # Main dashboard with analytics
│   ├── applications.py    # Job applications manager
│   ├── job_search.py      # Job search interface
│   ├── activities.py      # Activity tracking
│   └── about_me.py        # Personal profile page
├── files/                  # Static assets
│   └── profile.jpg        # Profile image
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (password, etc.)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deroso2017/career-manager-streamlit.git
   cd career-manager-streamlit
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add:
   ```
   PASSWORD=your_secure_password_here
   ```

5. **Run the application:**
   ```bash
   streamlit run main.py
   ```

The app will open in your default browser at `http://localhost:8501`

---

## 📋 Features

- **🔐 Secure Login** – Password-protected access to your applications
- **📊 Dashboard** – Visual overview of your job search progress
- **📝 Applications Manager** – Track all job applications with details
- **🔍 Job Search** – Centralized job search interface
- **📈 Activity Tracking** – Monitor your job search activities
- **👤 Profile Page** – Personal information and about section

---

## 📜 License

**All rights reserved.**

This project and its source code are proprietary and confidential. The code may not be copied, modified, distributed, published, sublicensed, or used for commercial or private purposes without prior written permission from the owner.

Unauthorized use of this software or any part of its source code is strictly prohibited.

For permission requests, please contact the owner.

---

## 📧 Contact

For inquiries or permission requests, please reach out to the project owner.

---

**Built as a learning project to demonstrate Python and Streamlit fundamentals.** 🎓
