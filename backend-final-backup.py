from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
import PyPDF2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
