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
