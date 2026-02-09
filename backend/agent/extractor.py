# agent/extractor.py
from langchain_ollama import ChatOllama
from agent.json_utils import extract_json

llm = ChatOllama(model="llama3.1:8b", temperature=0)

def extract_resume(resume_text: str):
    prompt = f"""
You are a resume parser.

RULES:
- Extract ONLY what exists in the resume
- DO NOT infer or guess missing data
- DO NOT rewrite or optimize wording
- DO NOT summarize
- Preserve original wording as much as possible
- Identify current role & company ONLY if explicitly present
- If a field is not found, return an empty string or empty list

RETURN STRICT JSON ONLY. No explanation. No markdown.

FORMAT:
{{
  "name": "",
  "headline": "",
  "contact": {{
    "email": "",
    "phone": ""
  }},
  "links": [],
  "summary": "",
  "current_role": "",
  "current_company": "",
  "work_experience": [
    {{
      "company": "",
      "role": "",
      "duration": "",
      "bullets": []
    }}
  ],
  "projects": [
    {{
      "name": "",
      "description": "",
      "bullets": []
    }}
  ],
  "skills": {{
    "Languages": [],
    "Frameworks": [],
    "Databases": [],
    "DevOps": [],
    "Tools": []
  }},
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ]
}}

RESUME TEXT:
{resume_text}
"""

    raw = llm.invoke(prompt).content
    data = extract_json(raw)

    if not data:
        raise ValueError("Resume extraction failed")

    return data
