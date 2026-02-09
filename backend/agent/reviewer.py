# agent/reviewer.py
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0)

REQUIRED_SECTIONS = [
    "work_experience",
    "projects",
    "skills",
    "education"
]


def review_resume(structured_resume: dict, job_desc: str):
    # 🔒 Structural validation first
    for section in REQUIRED_SECTIONS:
        if section not in structured_resume:
            return f"VERDICT: RETRY\nREASON: Missing section {section}"

    prompt = f"""
Review resume strictly against job description.

Return ONLY:

VERDICT: PASS or RETRY
REASON: one short sentence

RESUME:
{structured_resume}

JOB DESCRIPTION:
{job_desc}
"""

    return llm.invoke(prompt).content.strip()
