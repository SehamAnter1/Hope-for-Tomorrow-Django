# 🙌 Donations Platform with Zoom & DRF

A full-featured Donations Web App built with **Django** and **Django Rest Framework**, featuring:

- Secure JWT-based authentication
- Zoom integration for project-related sessions
- One-time donation payments
- Optional donor anonymity and custom messages
- OTP verification (optional or planned)
- Searchable, filterable donation projects

### 🧩 Zoom Integration
- Integration for project-related Zoom functionality (meetings, updates, etc.)
- Modular Zoom app with utility functions, models, views

---

## 🛠️ Tech Stack

- **Backend**: Django
- **Database**: SQLite 
- **Authentication**: JWT
---

## ⚙️ Setup

```bash
git clone https://github.com/sehamanter1/donation-platform.git
cd donation-platform
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
