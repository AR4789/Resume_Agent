# agent/optimizer.py
from langchain_ollama import ChatOllama
from agent.json_utils import extract_json

# 🔑 llm MUST be defined in this file
llm = ChatOllama(model="llama3.1:8b", temperature=0.2)

def optimize_resume(
    structured_resume: dict,
    job_desc: str,
    plan: dict,
    resume_type: str
):
    prompt = f"""
You are an expert resume optimizer.

RULES:
- Input resume is already extracted and factual
- Improve clarity, impact, and ATS alignment
- DO NOT add companies, roles, degrees, or dates
- DO NOT remove any section
- DO NOT modify or invent links
- Respect planner guidance: {plan}

PROFESSIONAL SUMMARY RULES:
- Write ONE paragraph only of minimum 3 lines and maximum 4 lines
- Each sentence should be concise and professional

RETURN STRICT JSON ONLY.

RESUME:
{structured_resume}

JOB DESCRIPTION:
{job_desc}
"""

    raw = llm.invoke(prompt).content
    data = extract_json(raw)

    if not data:
        raise ValueError("Optimizer failed to return valid JSON")

    return data
