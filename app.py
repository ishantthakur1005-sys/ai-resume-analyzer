import os
import json
import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)
    return "\n".join(pages_text)

def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an experienced technical recruiter and AI hiring manager.
    Compare the following candidate resume against the job description.

    Return ONLY valid JSON with these exact keys:
    {{
        "match_score": <integer from 0 to 100>,
        "summary": "<2-sentence honest assessment of fit>",
        "matching_skills": ["skill1", "skill2"],
        "missing_keywords": ["keyword1", "keyword2"],
        "resume_improvements": [
            "Actionable improvement 1",
            "Actionable improvement 2",
            "Actionable improvement 3"
        ]
    }}

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """

    models_to_try = [
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
    ]

    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            continue

    raise last_error
    return json.loads(response.text)


st.set_page_config(page_title="AI Resume & JD Analyzer", page_icon="📄", layout="centered")
st.title("📄 AI Resume & Job Description Analyzer")
st.write("Upload your resume (PDF) and paste a job description to get an instant skill-gap and ATS match analysis.")

uploaded_pdf = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description (JD)", height=200, placeholder="Paste the target role's responsibilities and required skills here...")

if st.button("Analyze Match", type="primary"):
    if not uploaded_pdf or not job_desc.strip():
        st.warning("Please upload a PDF resume and paste a job description first.")
    else:
        with st.spinner("Reading PDF and analyzing match..."):
            try:
                resume_text = extract_pdf_text(uploaded_pdf)
                result = analyze_resume(resume_text, job_desc)

                st.divider()
                st.metric(label="Overall Match Score", value=f"{result['match_score']}%")
                st.info(result["summary"])

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Matching Skills")
                    for skill in result["matching_skills"]:
                        st.markdown(f"- {skill}")

                with col2:
                    st.subheader("⚠️ Missing Keywords")
                    for kw in result["missing_keywords"]:
                        st.markdown(f"- {kw}")

                st.subheader("🚀 Actionable Resume Improvements")
                for tip in result["resume_improvements"]:
                    st.markdown(f"- {tip}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")