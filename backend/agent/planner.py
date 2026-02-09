def plan_resume(extracted_resume: dict, job_desc: str):
    prompt = f"""
Analyze resume vs job description.

Return JSON ONLY.

FORMAT:
{{
  "focus_sections": [],
  "missing_keywords": [],
  "tone": "professional",
  "seniority": ""
}}

RESUME:
{extracted_resume}

JOB DESCRIPTION:
{job_desc}
"""
