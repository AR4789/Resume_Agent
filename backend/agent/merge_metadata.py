def merge_metadata(resume: dict, metadata: dict) -> dict:
    """
    Merge deterministic metadata into extracted resume
    WITHOUT overwriting LLM-extracted content.

    Fixes:
    - Removes project links from header
    - Removes duplicate mailto email links
    """

    # ---------- CONTACT ----------
    resume.setdefault("contact", {})
    for k, v in metadata.get("contact", {}).items():
        if v and not resume["contact"].get(k):
            resume["contact"][k] = v

    # ---------- ALL LINKS ----------
    all_links = metadata.get("links", [])

    # ---------- PROJECT NAMES (for filtering) ----------
    project_names = {
        p.get("name", "").lower().replace(" ", "").replace("-", "").replace("_", "")
        for p in resume.get("projects", [])
        if p.get("name")
    }

    # ---------- HEADER LINKS (FILTERED) ----------
    raw_header_links = metadata.get("header_links", [])
    header_links = []

    for url in raw_header_links:
        u = url.lower()

        # ❌ Skip mailto links (email already shown)
        if u.startswith("mailto:"):
            continue

        # ❌ Skip project-related links
        key = u.replace("-", "").replace("_", "")
        if any(p in key for p in project_names):
            continue

        # ✅ Keep genuine profile / identity links
        header_links.append(url)

    # ---------- ASSIGN BACK ----------
    resume["header_links"] = header_links
    resume["links"] = all_links

    return resume
