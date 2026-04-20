<<<<<<< HEAD
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pdfplumber
from docx import Document
import io
=======
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
import PyPDF2
>>>>>>> 8941e7c (Final working version of AI Career Agent)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
<<<<<<< HEAD
=======
    allow_credentials=True,
>>>>>>> 8941e7c (Final working version of AI Career Agent)
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
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
    "data warehouse", "excel modeling", "pivot tables", "vlookup",
    "postgresql", "power query", "dax", "salesforce", "api integration"
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text)
    except Exception as e:
        return f"PDF extraction error: {str(e)}"
    return "\n".join(text_parts).strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
    except Exception as e:
        return f"DOCX extraction error: {str(e)}"

def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if lower_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

def generate_rewrite(job_title: str, job_description: str, resume_text: str, matched_skills: list[str], missing_skills: list[str]) -> str:
    if not resume_text.strip():
        return "No rewrite generated because no resume text could be extracted."

    summary = (
        f"Results-driven candidate targeting a {job_title} role with experience in "
        f"{', '.join(matched_skills[:4]) if matched_skills else 'data analysis, reporting, and problem solving'}."
    )

    bullet_1 = "Analyzed data and generated insights to support business decisions and reporting needs."
    bullet_2 = "Built dashboards, reports, and data summaries to track key performance indicators."
    bullet_3 = "Worked with structured data sources and queries to support analytical requests and recurring processes."
    bullet_4 = "Collaborated with stakeholders to communicate findings and improve data-driven workflows."

    if "sql" in matched_skills:
        bullet_3 = "Used SQL to extract, transform, and analyze data for business reporting and decision support."

    if "excel" in matched_skills:
        bullet_2 = "Built reports and performed data validation using Excel-based analysis and business reporting workflows."

    if "python" in matched_skills:
        bullet_4 = "Applied Python to support data analysis, automation, and process improvement tasks."

    if "power bi" in missing_skills:
        bullet_2 += " Strengthening Power BI dashboard development would further align with this role."

    return f"""
Professional Summary:
{summary}

Improved Bullet Points:
- {bullet_1}
- {bullet_2}
- {bullet_3}
- {bullet_4}
""".strip()

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
        resume_preview = raw_resume_text[:1000] if raw_resume_text else "No resume text extracted. This file may not be machine-readable."

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

    rewritten_resume = generate_rewrite(
        job_title=jobTitle,
        job_description=jobDescription,
        resume_text=raw_resume_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )

    return {
        "job_title": jobTitle,
        "match_score": match_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "resume_preview": resume_preview,
        "rewritten_resume": rewritten_resume
=======
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception:
        return ""
    return text

@app.post("/analyze")
async def analyze(
    resume: UploadFile = None,
    job_title: str = Form(None),
    job_description: str = Form(None)
):
    resume_text = ""

    if resume:
        content = await resume.read()
        filename = (resume.filename or "").lower()

        if filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(content)
        else:
            resume_text = content.decode("utf-8", errors="ignore")

    resume_skills = [
        "python", "sql", "excel", "data analysis",
        "communication", "aws", "git", "linux",
        "reporting", "visualization", "r", "power bi"
    ]

    job_skills = [
        "excel", "r", "scala", "healthcare",
        "erp", "implementation"
    ]

    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]

    score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

    rewrite = {
        "summary": (
            f"Results-driven candidate targeting a {job_title or 'target'} role with "
            f"experience in {', '.join(matched) if matched else 'data analysis'}. "
            f"Brings strong communication, analytical thinking, and a data-driven approach "
            f"to solving business problems."
        ),
        "bullets": [
            "Analyzed data and generated insights to support business decisions and operational reporting.",
            "Built dashboards, reports, and data summaries to track key performance indicators and improve visibility.",
            "Worked with structured data sources and business requirements to support analytical requests and recurring processes.",
            "Collaborated with stakeholders to communicate findings, improve workflows, and support implementation goals."
        ],
        "education": [
            "Kennesaw State University, Bachelor of Business in Information Systems, May 2026",
            "GPA: 3.4 | Dean’s List: Fall 2022, Spring 2024"
        ],
        "projects": [
            "AI Career Agent — Built a FastAPI and JavaScript application to analyze resumes against job descriptions and generate improvement recommendations.",
            "Global Economic Policy Project — Developed dashboards and data analysis workflows using SQL and Python to support simulations and decision-making."
        ]
    }

    return {
        "score": score,
        "job_title": job_title or "No title returned",
        "matched": matched,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing": missing,
        "suggestions": [f"Add or build experience with {s}" for s in missing],
        "resume_preview": resume_text[:1200] if resume_text else "No resume text extracted.",
        "rewrite_structured": rewrite
>>>>>>> 8941e7c (Final working version of AI Career Agent)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
