import streamlit as st
import requests
import json
import pandas as pd

# --- Configuration ---
# THIS IS THE FINAL, LIVE URL for your backend on Render.
BASE_URL = "https://smart-resume-screener-u2zt.onrender.com"

API_URL = f"{BASE_URL}/analyze"
TALENT_POOL_URL = f"{BASE_URL}/resumes"


# --- Predefined Job Data ---
jobs = [
    { "category": "Software Development and Engineering", "role": "Frontend Developer", "description": "Create user interfaces and implement visual elements.", "skills": ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "UI/UX", "Responsive Design"] },
    { "category": "Software Development and Engineering", "role": "Backend Developer", "description": "Build server-side logic and databases.", "skills": ["Python", "Java", "Node.js", "SQL", "APIs", "Django", "Flask", "Database Design"] },
    { "category": "Software Development and Engineering", "role": "Full Stack Developer", "description": "Handle both client and server-side development.", "skills": ["Frontend Tech", "Backend Tech", "Databases", "DevOps", "System Design", "APIs"] },
    { "category": "Software Development and Engineering", "role": "Mobile App Developer", "description": "Develop mobile applications for iOS and Android platforms.", "skills": ["Swift", "Kotlin", "React Native", "Flutter", "Mobile UI/UX", "App Store Deployment"] },
    { "category": "Software Development and Engineering", "role": "Game Developer", "description": "Create engaging and interactive games.", "skills": ["Unity", "Unreal Engine", "C++", "C#", "3D Graphics", "Game Physics"] },
    { "category": "Data Science and Analytics", "role": "Data Analyst", "description": "Transform data into insights", "skills": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"] },
    { "category": "Data Science and Analytics", "role": "Machine Learning Engineer", "description": "Build and deploy machine learning models", "skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Deep Learning"] },
    { "category": "Data Science and Analytics", "role": "Data Scientist", "description": "Analyze complex data sets to find patterns", "skills": ["Python", "R", "Machine Learning", "Statistics", "SQL", "Deep Learning"] },
    { "category": "Project Management", "role": "Product Manager", "description": "Define and drive product vision", "skills": ["Product Strategy", "Market Research", "User Stories", "Roadmapping"] },
    { "category": "Project Management", "role": "Project Manager", "description": "Lead and manage project delivery", "skills": ["Project Planning", "Agile", "Scrum", "Risk Management", "Stakeholder Management"] },
    { "category": "Cybersecurity", "role": "Security Analyst", "description": "Monitor and protect against security threats", "skills": ["Network Security", "Threat Detection", "Security Tools", "Incident Response"] },
    { "category": "Cybersecurity", "role": "Penetration Tester", "description": "Test systems for security vulnerabilities", "skills": ["Ethical Hacking", "Security Tools", "Network Security", "Web Security"] },
    { "category": "UI/UX Design", "role": "UX Designer", "description": "Design user experiences and flows", "skills": ["User Research", "Wireframing", "Prototyping", "Usability Testing"] },
    { "category": "UI/UX Design", "role": "UI Designer", "description": "Create beautiful user interfaces", "skills": ["Figma", "Adobe XD", "Visual Design", "Typography", "Color Theory"] },
    { "category": "Cloud Computing and DevOps", "role": "Cloud Architect", "description": "Design and manage cloud infrastructure", "skills": ["AWS", "Azure", "GCP", "Infrastructure as Code", "Security"] },
    { "category": "Cloud Computing and DevOps", "role": "Site Reliability Engineer", "description": "Ensure system reliability and performance", "skills": ["Linux", "Monitoring", "Automation", "Performance Tuning", "Incident Response"] },
    { "category": "Cloud Computing and DevOps", "role": "DevOps Engineer", "description": "Implement DevOps practices and tools", "skills": ["Docker", "Kubernetes", "CI/CD", "Automation", "Monitoring"] }
]

# --- API Communication Function ---
def call_analysis_api(job_description, resume_file):
    try:
        files = {'resume': (resume_file.name, resume_file.getvalue(), resume_file.type)}
        data = {'job_description': job_description}
        response = requests.post(API_URL, files=files, data=data, timeout=90)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to the backend API. It might be starting up. Please wait and try again. Error: {e}")
        return None

# --- Streamlit App UI ---
st.set_page_config(page_title="Smart Resume Screener", page_icon="📄", layout="wide")

# --- UPDATED BEAUTIFUL CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* General Styling */
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp { 
        background-color: #0E1117; 
        color: #FAFAFA;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #161B22;
        border-right: 1px solid #30363d;
    }

    /* Main Title with Glow Effect */
    h1 {
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 163, 108, 0.5), 0 0 20px rgba(0, 163, 108, 0.3);
    }
    
    h2, h3 {
        font-weight: 600;
        color: #C9D1D9;
        border-bottom: 1px solid #30363d;
        padding-bottom: 10px;
    }

    /* Result Card Styling */
    .result-card { 
        background: linear-gradient(145deg, #21262d, #161b22);
        border-radius: 12px; 
        padding: 25px; 
        margin-bottom: 20px; 
        box-shadow: 5px 5px 15px #0d0f13, -5px -5px 15px #2b313b;
        border: 1px solid #30363d;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-5px);
        border-color: #00A36C;
    }

    /* Buttons and Links */
    .stButton>button, a.template-link {
        font-weight: 600;
        background-color: #00A36C; 
        color: white; 
        border-radius: 25px; 
        border: 1px solid #00A36C; 
        padding: 12px 28px; 
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 163, 108, 0.4);
    }
    .stButton>button:hover, a.template-link:hover {
        background-color: #007A53;
        color: white; 
        border: 1px solid #007A53;
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 163, 108, 0.6);
    }
    
    /* Score Badge */
    .score-badge { 
        display: inline-block; 
        padding: 10px 20px; 
        border-radius: 25px; 
        color: white; 
        font-size: 22px; 
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div { background-color: #00A36C; }
    
    /* Expander Styling */
    [data-testid="stExpander"] {
        border: 1px solid #30363d;
        border-radius: 8px;
        background-color: #161B22;
    }
</style>
""", unsafe_allow_html=True)


# --- Robust Logic for Templates ---
query_params = st.query_params
if "template" in query_params:
    template_role = query_params["template"].replace("_", " ")
    selected_job_details = next((job for job in jobs if job['role'] == template_role), None)
    if selected_job_details:
        jd_text = (f"**Role:** {selected_job_details['role']}\n\n"
                   f"**Description:** {selected_job_details['description']}\n\n"
                   f"**Key Skills:**\n- " + "\n- ".join(selected_job_details['skills']))
        st.session_state.job_description = jd_text
        st.query_params.clear()

# --- Main Application Logic ---
st.title("📄 Smart Resume Screener")

tab1, tab2 = st.tabs(["Analyze New Resumes", "View Talent Pool (Database)"])

with tab1:
    st.header("Analyze New Resumes")

    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'shortlist_threshold' not in st.session_state:
        st.session_state.shortlist_threshold = 75

    with st.sidebar:
        st.header("Controls")
        with st.expander("Use a Job Description Template", expanded=True):
            categories = sorted(list(set(job['category'] for job in jobs)))
            selected_category = st.selectbox("Select a Job Category", categories)
            roles_in_category = sorted([job['role'] for job in jobs if job['category'] == selected_category])
            selected_role = st.selectbox("Select a Job Role", roles_in_category)
            
            role_slug = selected_role.replace(" ", "_")
            st.markdown(f'<a href="?template={role_slug}" class="template-link" target="_self" style="display: block; text-align: center; text-decoration: none;">Use this Template</a>', unsafe_allow_html=True)

        job_description = st.text_area("Enter the Job Description Here", value=st.session_state.job_description, height=300, placeholder="Select a template or paste the job description...", key="job_desc_main")
        st.session_state.job_description = job_description

        uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type=["pdf"], accept_multiple_files=True)
        
        st.markdown("---")
        st.header("Shortlisting")
        st.session_state.shortlist_threshold = st.number_input("Display candidates with score above:", min_value=0, max_value=100, value=st.session_state.shortlist_threshold, key='threshold_input')
        
        analyze_button = st.button("Analyze Resumes")
        
    if analyze_button:
        if not st.session_state.job_description.strip():
            st.error("❌ Please provide a job description before analyzing.")
            st.stop()
        if not uploaded_files:
            st.error("❌ Please upload at least one resume before analyzing.")
            st.stop()
            
    if analyze_button and uploaded_files and st.session_state.job_description.strip():
        st.session_state.results = [] 
        total_files = len(uploaded_files)
        progress_bar = st.progress(0, text="Starting analysis...")

        for i, uploaded_file in enumerate(uploaded_files):
            file_name = uploaded_file.name
            progress_text = f"Contacting API for {file_name} ({i+1}/{total_files})..."
            progress_bar.progress((i + 1) / total_files, text=progress_text)

            with st.spinner(progress_text):
                analysis = call_analysis_api(st.session_state.job_description, uploaded_file)
                if analysis:
                    st.session_state.results.append({
                        "file_name": file_name,
                        "score": analysis.get("match_score", 0),
                        "summary": analysis.get("justification", "No summary provided."),
                        "skills": analysis.get("extracted_skills", []),
                        "experience": analysis.get("extracted_experience", "Not found."),
                        "education": analysis.get("extracted_education", "Not found."),
                        "missing": analysis.get("missing_keywords", [])
                    })
        progress_bar.empty()

    if st.session_state.results:
        st.session_state.results.sort(key=lambda x: x['score'], reverse=True)
        shortlisted_candidates = [r for r in st.session_state.results if r.get('score', 0) >= st.session_state.shortlist_threshold]

        if shortlisted_candidates:
            st.header(f"🏆 Shortlisted Candidates (Score >= {st.session_state.shortlist_threshold}%)")
            st.subheader("Quick View")
            st.markdown("- " + "\n- ".join([c['file_name'] for c in shortlisted_candidates]))
            st.markdown("---")
            st.subheader("Detailed Analysis")
            
            for result in shortlisted_candidates:
                score = result.get('score', 0)
                if score >= 85: badge_color = "#28a745"
                elif score >= 70: badge_color = "#ffc107"
                else: badge_color = "#dc3545"

                st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f'<h5>{result["file_name"]}</h5>', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-badge" style="background-color:{badge_color};">{score}%</div>', unsafe_allow_html=True)
                with col2:
                    with st.expander("**View Detailed Analysis**", expanded=(score >= 85)):
                        st.info(result['summary'])
                        if result.get('skills'): st.success(f"**Skills:** {', '.join(result['skills'])}")
                        if result.get('experience'): st.write(f"**Experience:** {result['experience']}")
                        if result.get('education'): st.write(f"**Education:** {result['education']}")
                        if result.get('missing'): st.warning("**Missing from Resume:**\n" + "\n".join(f"- {k}" for k in result['missing']))
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif st.session_state.results:
            st.warning(f"No candidates meet the score threshold of {st.session_state.shortlist_threshold}%. Try a lower score.")
    
    elif not analyze_button:
        st.info("Upload resumes and a job description, then click 'Analyze Resumes' to see the results here.")

# --- Talent Pool Tab ---
with tab2:
    st.header("🗂️ View Talent Pool (from Database)")
    st.write("This section shows all resumes that have been previously analyzed and stored in the database.")
    
    if st.button("Refresh Data from Database"):
        try:
            response = requests.get(TALENT_POOL_URL, timeout=30)
            if response.status_code == 200:
                data = response.json()
                st.session_state.talent_pool_data = data
                st.success(f"Successfully loaded {len(data)} records from the database!")
            else:
                st.error(f"Failed to fetch data from API: {response.status_code}")
        except requests.exceptions.RequestException:
            st.error("Connection Error: Could not connect to the backend API. Is it running?")

    if 'talent_pool_data' in st.session_state and st.session_state.talent_pool_data:
        df = pd.DataFrame(st.session_state.talent_pool_data)
        st.dataframe(df[['filename', 'match_score', 'analysis_date', 'justification', 'extracted_skills', 'missing_keywords']])
    else:
        st.info("Click the 'Refresh' button to load analyzed candidates from the database.")

