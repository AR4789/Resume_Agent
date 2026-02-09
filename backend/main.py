from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from utils import read_pdf, read_docx
from resume_export import save_optimized_resume
from apply import apply_via_email, generate_cover_letter
from config import HUMAN_APPROVAL_REQUIRED, AUTO_APPLY_ENABLED
from ats.scorer import ats_score
from agent.orchestrator import run_agent
from agent.resume_metadata import extract_resume_metadata
from ats.email_validator import is_valid_email
from fastapi.staticfiles import StaticFiles




try:
    from linkedin.apply import apply_linkedin_job
    LINKEDIN_ENABLED = True
except Exception:
    LINKEDIN_ENABLED = False


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/resumes",
    StaticFiles(directory="resumes"),
    name="resumes"
)


@app.post("/optimize")
async def optimize(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    company: str = Form(...),
    role: str = Form(...),
    applicant_name: str = Form(...),
    resume_type: str = Form("normal"),
    design: str = Form("modern"), 
    density: str = Form("detailed"), 
    apply_email: str = Form(None),
):
    content = await resume.read()

    # Always return TEXT ONLY
    if resume.filename.lower().endswith(".pdf"):
        resume_text = read_pdf(content)
    else:
        resume_text = read_docx(content)

    # 🔑 FastAPI now passes ONLY raw inputs
    structured_resume, review = run_agent(
        resume_text=resume_text,
        pdf_bytes=content,
        job_desc=job_description,
        resume_type=resume_type
    )

    output_path = f"resumes/optimized/{resume.filename}"
    save_optimized_resume(structured_resume, output_path,design=design,density=density)

    ats = ats_score(resume_text, job_description)

    applied = False
    email_error = None

    if AUTO_APPLY_ENABLED and not HUMAN_APPROVAL_REQUIRED and apply_email:
        if not is_valid_email(apply_email):
            email_error = "Invalid email address"
        else:
            cover_letter = generate_cover_letter(
                applicant_name,
                company,
                role,
                structured_resume,
                job_description
            )
            apply_via_email(
                apply_email,
                output_path,
                cover_letter,
                company,
                role,
                applicant_name
            )
            applied = True

    return {
        "resume_file": resume.filename,
        "resume_download_url": f"/resumes/optimized/{resume.filename}",
        "structured_resume": structured_resume,
        "ats": ats,
        "applied": applied,
        "email_error": email_error
    }
