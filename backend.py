from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pdfplumber
from docx import Document
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

skills_list = [
    "python", "sql", "excel", "tableau", "power bi", "data analysis",
    "machine learning", "statistics", "pandas", "numpy", "matplotlib",
    "data visualization", "visualization", "r", "spark", "aws",
    "data engineering", "etl", "big data", "hadoop", "dashboard",
    "analytics", "business intelligence", "forecasting", "a/b testing",
    "snowflake", "looker", "dbt", "airflow", "databricks", "git",
    "linux", "java", "c++", "scala", "sas", "claims", "insurance",
    "healthcare", "reporting", "kpi", "data mining", "predictive modeling",
    "deep learning", "nlp", "tensorflow", "pytorch", "crm", "erp",
    "auditing", "risk analysis", "financial modeling", "communication",
    "presentation", "problem solving", "querying", "warehousing",
    "data warehouse", "excel modeling", "pivot tables", "vlookup"
]

def extract_text_from_pdf(file_bytes):
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text)
    except Exception as e:
        return f"PDF extraction error: {str(e)}"

    full_text = "\n".join(text_parts).strip()
    if not full_text:
        return ""
    return full_text

def extract_text_from_docx(file_bytes):
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text.strip()
    except Exception as e:
        return f"DOCX extraction error: {str(e)}"

def extract_resume_text(filename, file_bytes):
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

@app.post("/analyze")
async def analyze(
    jobTitle: str = Form(...),
    jobDescription: str = Form(...),
    resume: UploadFile = File(...)
):
    file_bytes = await resume.read()
    raw_resume_text = extract_resume_text(resume.filename, file_bytes)

    if raw_resume_text.startswith("PDF extraction error:") or raw_resume_text.startswith("DOCX extraction error:"):
        resume_text = ""
        resume_preview = raw_resume_text
    else:
        resume_text = raw_resume_text.lower()
        resume_preview = raw_resume_text[:1000] if raw_resume_text else "No resume text extracted. This PDF may be image-based or not machine-readable."

    job_text = jobDescription.lower()

    resume_skills = []
    job_skills = []

    for skill in skills_list:
        if skill in resume_text:
            resume_skills.append(skill)
        if skill in job_text:
            job_skills.append(skill)

    resume_skills = list(dict.fromkeys(resume_skills))
    job_skills = list(dict.fromkeys(job_skills))

    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    total_required = len(job_skills)
    matched = len(matched_skills)

    match_score = int((matched / max(3, total_required)) * 100)
    if match_score > 100:
        match_score = 100

    suggestions = [f"Add or build experience with {skill}" for skill in missing_skills[:5]]

    return {
        "job_title": jobTitle,
        "match_score": match_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "resume_preview": resume_preview
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
