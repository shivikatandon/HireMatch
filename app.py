# app.py
import streamlit as st
import fitz  # PyMuPDF for PDF
from docx import Document  # python-docx for DOCX
import re

def extract_text_from_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    text = ""
    doc = Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return ""

def load_skills_list():
    return [
        "python", "pandas", "numpy", "r", "sql", "excel",
        "power bi", "tableau", "machine learning", "deep learning",
        "nlp", "generative ai", "llms", "computer vision",
        "data cleaning", "data visualization", "eda", "automation", "c++", "spark", "pyspark", "kafka"
    ]

def extract_skills(text, skills_master):
    text = text.lower()
    found = []
    for skill in skills_master:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
            found.append(skill)
    return found

def evaluate_resume(resume_text, jd_text, skills_master):
    jd_skills = set(extract_skills(jd_text, skills_master))
    resume_skills = set(extract_skills(resume_text, skills_master))

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    # Verdict
    if score >= 70:
        verdict = "High"
    elif score >= 40:
        verdict = "Medium"
    else:
        verdict = "Low"

    return score, verdict, matched, missing

# =====================
# Streamlit App
# =====================
st.set_page_config(page_title="HireMatch", page_icon="📝", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>HireMatch</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Automated Resume Checker</h3>", unsafe_allow_html=True)

st.write("### 📄 Upload a Job Description")
jd_file = st.file_uploader("Upload JD (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

st.write("### 🧑‍🎓 Upload Resumes")
resume_files = st.file_uploader("Upload multiple resumes (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"], accept_multiple_files=True)

if jd_file and resume_files:
    jd_text = extract_text(jd_file)
    skills_master = load_skills_list()

    results = []
    for resume_file in resume_files:
        resume_text = extract_text(resume_file)
        score, verdict, matched, missing = evaluate_resume(resume_text, jd_text, skills_master)

        results.append({
            "Resume": resume_file.name,
            "🎯 Score (%)": score,
            "📊 Verdict": verdict,
            "✅ Matched Skills": ", ".join(matched),
            "❌ Missing Skills": ", ".join(missing)
        })

    st.write("## 📊 Resume Evaluations")
    st.dataframe(results)

    # Highlight best match
    best = max(results, key=lambda x: x["🎯 Score (%)"])
    st.success(f"🏆 Best Match: **{best['Resume']}** 🎯 Score: {best['🎯 Score (%)']}% | Verdict: {best['📊 Verdict']}")
