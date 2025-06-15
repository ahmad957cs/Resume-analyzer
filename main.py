import streamlit as st
import PyPDF2
import docx
import re
import spacy

# Load spaCy model for name extraction
nlp = spacy.load("en_core_web_sm")

# Common skills including GoHighLevel, banking, and teaching
common_skills = [
    "python", "java", "javascript", "html", "css", "sql", "management",
    "leadership", "communication", "analysis", "project management",
    "microsoft office", "excel", "word", "powerpoint", "automation",
    "funnels", "crm", "email marketing", "zapier", "go high level",
    "ghl", "a2p", "saas", "stripe", "banking", "loan", "compliance",
    "accounting", "finance", "teacher", "lesson planning", "classroom",
    "curriculum", "education", "student engagement"
]

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_info(text):
    doc = nlp(text)

    # Extract name (first person entity with 2+ words)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
            name = ent.text.strip()
            break

    # Extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    email = email_match.group(0) if email_match else None

    # Extract phone number with optional country code
    phone_pattern = r'(\+\d{1,3}[-\s]?)?\(?\d{2,4}\)?[-\s]?\d{3,5}[-\s]?\d{4,6}'
    phone_match = re.search(phone_pattern, text)
    phone = phone_match.group(0) if phone_match else None

    # Extract skills
    found_skills = []
    lower_text = text.lower()
    for skill in common_skills:
        if skill.lower() in lower_text:
            found_skills.append(skill)

    return name, email, phone, list(set(found_skills))

def rate_resume(name, email, phone, skills):
    score = 0
    feedback = []

    if name:
        score += 25
    else:
        feedback.append("Missing name")

    if email:
        score += 25
    else:
        feedback.append("Missing email")

    if phone:
        score += 25
    else:
        feedback.append("Missing phone number")

    if skills:
        score += 25 * (min(len(skills), 3) / 3)
    else:
        feedback.append("No skills identified")

    return score, feedback

def suggest_job_positions(skills):
    ghl_skills = {"go high level", "crm", "funnels", "email marketing", "automation", "a2p", "ghl"}
    banking_skills = {"finance", "banking", "loan", "compliance", "accounting"}
    teaching_skills = {"teacher", "lesson planning", "classroom", "curriculum", "education"}

    suggested = []
    lower_skills = {s.lower() for s in skills}

    if ghl_skills & lower_skills:
        suggested.append("GoHighLevel Automation Expert")
    if banking_skills & lower_skills:
        suggested.append("Banking & Financial Analyst")
    if teaching_skills & lower_skills:
        suggested.append("Educator / Teacher / Instructor")

    if not suggested:
        suggested.append("General Role (Based on Skills)")

    return suggested

def main():
    # Background Gradient CSS
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #621C72 0%, #511B77 50%, #8F258D 100%);
            color: white;
        }
        /* Override default text color in some components */
        .stTextInput>div>div>input, .stTextInput>div>div>textarea {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
        }
        .stTextInput>label {
            color: white;
        }
        .stButton>button {
            background-color: #8F258D;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📄 Smart Resume Analyzer & Job Predictor")

    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

        name, email, phone, skills = extract_info(text)

        st.subheader("🧾 Resume Data Extracted:")

        # Allow manual correction
        if not name:
            name = st.text_input("Name not found. Please enter your name:")

        if not email:
            email = st.text_input("Email not found. Please enter your email:")

        if not phone:
            phone = st.text_input("Phone number not found. Please enter your phone number:")

        if not skills:
            skills_input = st.text_input("No skills found. Enter your skills (comma-separated):")
            if skills_input:
                skills = [skill.strip() for skill in skills_input.split(",")]

        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")
        st.write(f"**Skills:** {', '.join(skills) if skills else 'None found'}")

        score, feedback = rate_resume(name, email, phone, skills)

        st.subheader("📊 Resume Score")
        st.success(f"Score: {score}/100")

        if feedback:
            st.subheader("🛠️ Feedback")
            for item in feedback:
                st.warning(f"- {item}")

        st.subheader("💼 Job Positions You Can Be Hired For:")
        job_positions = suggest_job_positions(skills)
        for job in job_positions:
            st.info(f"- {job}")

        st.markdown("---")
        st.write("✅ To improve your resume, include contact info and 3–5 strong skills related to the job you're targeting.")

if __name__ == "__main__":
    main()
