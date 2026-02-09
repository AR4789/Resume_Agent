import re

def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return set(words)

def ats_score(resume_text, job_desc):
    resume_keys = extract_keywords(resume_text)
    job_keys = extract_keywords(job_desc)

    matched = resume_keys & job_keys
    score = int((len(matched) / max(len(job_keys), 1)) * 100)

    return {
        "ats_score": score,
        "matched_keywords": list(matched),
        "missing_keywords": list(job_keys - resume_keys)
    }
