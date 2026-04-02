# 🚀 AI Investor Outreach CRM

A full-stack AI-powered CRM to manage investor outreach, track interactions, and generate smart follow-ups.

---

## ✨ Features

### 📌 Lead Management
- Add investor leads (name, email, LinkedIn, net worth tier, interests)
- Track lead stages:
  - Cold → Contacted → Interested → Committed

### 📞 Interaction Tracking
- Log calls, emails, meetings
- Maintain complete history per investor

### ⏰ Smart Reminders
- Automatically generate follow-up reminders
- Prevent duplicate reminders
- Priority-based alerts (High / Medium / Low)

### 🤖 AI Features
- ✉️ Auto-generate follow-up emails
- 🧠 Summarize interaction history
- 📊 Lead scoring system
- 🔥 Next best action recommendations

---

## 🏗️ Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Database:** SQLite  
- **AI:** LLM-based prompt system  
- **Containerization:** Docker + Docker Compose  

---

## ⚙️ Setup & Running

---

### 🥇 Option 1: Run with Docker (Recommended)

#### 1. Install Docker
Download: https://www.docker.com/products/docker-desktop

---

#### 2. Run the app

```bash
docker-compose up --build