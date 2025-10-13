import os
import json
import sqlite3
from flask import Flask, request, jsonify
import google.generativeai as genai
import PyPDF2
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() 

try:
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in .env file or environment variables.")
    genai.configure(api_key=API_KEY)
except ValueError as e:
    print(f"Configuration Error: {e}")
    exit()

app = Flask(__name__)
DATABASE = 'resumes.db'

# --- Database Functions ---
def get_db_connection():
    # Render's file system can be ephemeral. For a real production app, you'd use a managed database
    # or a persistent disk. For this project, we'll create the DB in the same directory.
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                job_description TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                justification TEXT,
                extracted_skills TEXT,
                extracted_experience TEXT,
                extracted_education TEXT,
                missing_keywords TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        db.commit()
        db.close()
        print("Database initialized.")

# --- THIS IS THE CRITICAL FIX ---
# Initialize the database when the application starts.
# This code runs whether you use "python api.py" or Gunicorn on Render.
init_db()

# --- Helper Functions ---
def extract_text_from_pdf(file_stream):
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def get_llm_analysis(resume_text, job_description):
    """
    Uses Google Gemini to extract structured data from the resume against the job description.
    """
    prompt = f"""
    You are an expert technical recruiter and talent analyst. Your task is to analyze the following resume against the provided job description and extract structured data.
    Your response must be a single, clean JSON object and nothing else. Do not wrap it in markdown.

    The JSON object must have these exact keys:
    - "match_score": (Integer) A score from 0 to 100.
    - "justification": (String) A concise paragraph justifying the score.
    - "extracted_skills": (List of Strings) Key technical skills from the resume.
    - "extracted_experience": (String) A brief summary of professional experience.
    - "extracted_education": (String) A brief summary of the highest education.
    - "missing_keywords": (List of Strings) Key skills from the job description missing from the resume.

    Job Description:
    ---
    {job_description}
    ---

    Resume:
    ---
    {resume_text}
    ---
    """
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
        
        response = model.generate_content(
            prompt, 
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        return json.loads(response.text)
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return None

# --- API Endpoints ---
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part"}), 400
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')
    if resume_file.filename == '' or not job_description:
        return jsonify({"error": "Missing file or job description"}), 400

    resume_stream = BytesIO(resume_file.read())
    resume_text = extract_text_from_pdf(resume_stream)
    if not resume_text:
        return jsonify({"error": "Could not extract text from PDF"}), 500

    analysis_result = get_llm_analysis(resume_text, job_description)
    if not analysis_result:
        return jsonify({"error": "Failed to get analysis from the language model"}), 500
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO analyses (filename, job_description, match_score, justification, 
                                  extracted_skills, extracted_experience, extracted_education, missing_keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            resume_file.filename,
            job_description,
            analysis_result.get('match_score'),
            analysis_result.get('justification'),
            json.dumps(analysis_result.get('extracted_skills', [])),
            analysis_result.get('extracted_experience'),
            analysis_result.get('extracted_education'),
            json.dumps(analysis_result.get('missing_keywords', []))
        ))
        db.commit()
        db.close()
    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify(analysis_result), 200

    return jsonify(analysis_result), 200

@app.route('/resumes', methods=['GET'])
def get_all_resumes():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM analyses ORDER BY analysis_date DESC")
        analyses = cursor.fetchall()
        db.close()
        return jsonify([dict(row) for row in analyses])
    except Exception as e:
        return jsonify({"error": f"Database fetch error: {e}"}), 500

# --- Main execution block for local testing ---
if __name__ == '__main__':
    # When you run "python api.py", this block runs the test server.
    # Gunicorn ignores this block and just uses the 'app' object.
    app.run(host='0.0.0.0', port=5000, debug=True)
