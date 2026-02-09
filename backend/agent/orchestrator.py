from agent.extractor import extract_resume
from agent.normalizer import normalize_resume
from agent.planner import plan_resume
from agent.optimizer import optimize_resume
from agent.reviewer import review_resume
from agent.resume_metadata import extract_resume_metadata
from agent.merge_metadata import merge_metadata  # small helper

def run_agent(
    resume_text: str,
    pdf_bytes: bytes | None,
    job_desc: str,
    resume_type: str
):
    # 1️⃣ Extract factual content via LLM
    extracted = extract_resume(resume_text)

    # 2️⃣ Deterministically extract links + contact
    metadata = extract_resume_metadata(resume_text, pdf_bytes)

    # 3️⃣ Merge metadata (links/contact only)
    extracted = merge_metadata(extracted, metadata)

    # 4️⃣ Normalize structure (NO content changes)
    normalized = normalize_resume(extracted)

    # 5️⃣ Analyze resume vs JD (advisory only)
    plan = plan_resume(normalized, job_desc)

    # 6️⃣ Optimize wording (NO new data)
    optimized = optimize_resume(
        normalized,
        job_desc,
        plan,
        resume_type
    )

    optimized["contact"] = normalized.get("contact", {})
    optimized["header_links"] = normalized.get("header_links", [])
    # 7️⃣ Final gate
    review = review_resume(optimized, job_desc)

    return optimized, review
