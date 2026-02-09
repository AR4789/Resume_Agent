import json
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0.3)

APPLICATION_LOG = "applications.json"

EMAIL_USER = "amanr1871@gmail.com"
EMAIL_PASS = "bmnvmseonnerdekv"

def log_application(data):
    try:
        with open(APPLICATION_LOG, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(data)

    with open(APPLICATION_LOG, "w") as f:
        json.dump(logs, f, indent=2)

def apply_via_email(to_email, resume_path, cover_letter, company, role, applicant_name):
    msg = EmailMessage()
    msg["Subject"] = f"Application for {role} – {applicant_name}"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    msg.set_content(cover_letter)

    with open(resume_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(resume_path)
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    log_application({
        "applicant": applicant_name,
        "company": company,
        "role": role,
        "resume_used": resume_path,
        "applied_on": datetime.now().isoformat(),
        "status": "APPLIED"
    })

def generate_cover_letter(name, company, role, resume_data, job_desc):
    prompt = f"""
You are a professional cover letter writer.

STRICT RULES:
- Output ONLY the cover letter text
- Do NOT include introductions like "Here is a cover letter"
- Do NOT include explanations or commentary
- Do NOT use markdown
- Start the letter with "Dear Hiring Manager"
- End the letter with "Sincerely," followed by the applicant's name
- Tone must be professional, confident, and human
- Length: 300–400 words

Applicant Name: {name}
Company: {company}
Role: {role}

Resume Data:
{resume_data}

Job Description:
{job_desc}
"""

    response = llm.invoke(prompt).content.strip()

    # ✅ HARD SAFETY CLEANUP (extra protection)
    if "Dear" in response:
        response = response[response.index("Dear"):]

    return response
