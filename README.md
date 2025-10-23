# Smart Resume Screener

A system that automatically screens resumes and job descriptions using an LLM (Large Language Model) to find the best candidate matches.

---

## 🚀 Features
- Accepts **PDF or text resumes** as input.
- Accepts **job description** as input.
- Extracts structured data (skills, experience, education) from resumes.
- Uses **LLM (OpenAI API)** for semantic matching and scoring.
- Displays **shortlisted candidates** with justification.
- Stores parsed resumes in a **SQLite database**.
- Backend implemented in **Python (FastAPI / Streamlit backend)**.
- Provides an optional **frontend dashboard** for visualization.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Streamlit** for frontend
- **SQLite** for database
- **OpenAI API** for LLM
- **dotenv** for environment variables

---

## ⚙️ Setup Instructions

### 1️⃣ Clone or extract the project
```bash
git clone https://github.com/Ruthiksmk/smartresume.git
cd smartresume



## 🚀 Live Demo
You can try the Smart Resume Screener app here:  
👉 [Smart Resume Screener on Streamlit](https://smartresume-tbwzygpcczraimvzqnukx4.streamlit.app/)

> ⚠️ *Note: If the app takes time to load or shows an error initially, please refresh the page once — Streamlit servers may sleep when inactive.*

## 🎥 Project Demo Video
Watch the demo video here:  
🎬 [Google Drive - Smart Resume Screener Demo](https://drive.google.com/file/d/1ip_CocD08kgIfMfOsvs84NkL7xg-NwU0/view?usp=sharing)



## 🧠 About the Project

This project automatically analyzes resumes and job descriptions using OpenAI’s GPT model to shortlist candidates based on job requirements.  
It features a Streamlit-based frontend and integrates a lightweight backend API for resume parsing and scoring.
