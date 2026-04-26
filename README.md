# 🔍 Job Skill Analyzer — GenAI Edition

> An AI-powered web application that analyzes skill gaps for tech roles and generates personalized learning roadmaps using **Google Gemini LLM**.

[![Live Demo](https://job-skill-analyzer-xyrvpw89rbsutlubr2rad9.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?style=for-the-badge&logo=google)](https://aistudio.google.com)

---

## 📌 Overview

Job Skill Analyzer helps CS students and job seekers identify exactly what skills they are missing for their target role — and then uses **Google Gemini AI** to tell them what to learn first, how to learn it, and answers any career questions they have.

Built with a modular pipeline for data processing, a market-demand scoring engine, and three distinct GenAI features powered by prompt engineering.

---

## ✨ Features

### 📊 Skill Gap Analysis
- Enter your current skills and select a target role
- Instantly see which skills you're missing, ranked by **market demand score**
- Categorized by skill type (Data Analysis, Visualization, ML, etc.)

### 🎯 AI Skill Prioritizer *(Powered by Gemini)*
- Ranks your missing skills from most to least important for hiring
- Labels each skill as 🔴 Critical / 🟡 Important / 🟢 Nice-to-have
- Gives a one-line reason for each ranking

### 🗓️ 4-Week Learning Roadmap *(Powered by Gemini)*
- Generates a personalized day-by-day study plan
- Includes **free resources only** (Khan Academy, YouTube, official docs)
- Ends with a "Quick Win" — something actionable to start today

### 💬 CareerBot *(Powered by Gemini)*
- Multi-turn AI chatbot with full conversation memory
- Ask about interview tips, salary, projects, tools — anything career related
- Role-aware: responses tailored to your specific target role

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Data Processing | Python, Pandas |
| AI / LLM | Google Gemini 2.5 (google-genai SDK) |
| Prompt Engineering | Structured prompt templates |
| Deployment | Streamlit Cloud |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
job-skill-analyzer/
├── app.py                  # Main Streamlit app with GenAI features
├── main.py                 # CLI version of the analyzer
├── src/
│   └── skill_gap_engine_06.py  # Core skill gap ranking engine
├── outputs/
│   └── week4_market_insights.csv  # Market demand dataset
├── data/                   # Raw data files
├── notebooks/              # Jupyter notebooks for EDA and analysis
├── assets/                 # Static assets
├── requirements.txt
└── README.md
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/srishtis2200/job-skill-analyzer.git
cd job-skill-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
# Create .streamlit/secrets.toml and add:
# GEMINI_API_KEY = "your-key-here"
# Get a free key at: https://aistudio.google.com/app/apikey

# 4. Run the app
streamlit run app.py
```

---

## 🎯 Supported Roles

- Data Analyst
- Data Scientist  
- Machine Learning Engineer
- Data Engineer

---
