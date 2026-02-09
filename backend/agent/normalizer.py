# agent/normalizer.py

def normalize_resume(data: dict):
    # Ensure lists exist but DO NOT inject fake values
    data.setdefault("work_experience", [])
    data.setdefault("projects", [])
    data.setdefault("education", [])

    skills = data.get("skills", {})
    for k in ["Languages", "Frameworks", "Databases", "DevOps", "Tools"]:
        skills.setdefault(k, [])

    data["skills"] = skills

    return data
