# agent/resume_metadata.py
import re
import io
from pypdf import PdfReader

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\+?\d[\d\s\-]{8,}\d"


def extract_pdf_annotation_links(bytes_data: bytes):
    links = []
    reader = PdfReader(io.BytesIO(bytes_data))

    for page in reader.pages:
        if "/Annots" not in page:
            continue

        for annot in page["/Annots"]:
            obj = annot.get_object()
            action = obj.get("/A")

            if not action:
                continue

            # Case 1: Standard URI
            if "/URI" in action:
                links.append(action["/URI"])

            # Case 2: GoToR / Launch links (VERY COMMON)
            elif "/F" in action:
                target = action["/F"]
                if isinstance(target, str) and target.startswith("http"):
                    links.append(target)

    return links



def extract_resume_metadata(resume_text: str, pdf_bytes: bytes | None = None):
    lines = resume_text.splitlines()

    text_links = []
    annotation_links = []

    # ---- TEXT URLS (usually project links) ----
    for idx, line in enumerate(lines):
        for u in re.findall(r"https?://[^\s|)>]+", line):
            text_links.append({
                "url": u.rstrip(".,)"),
                "line_index": idx
            })

    # ---- PDF ANNOTATION LINKS (HEADER LINKS) ----
    if pdf_bytes:
        for u in extract_pdf_annotation_links(pdf_bytes):
            annotation_links.append(u)

    # 🔑 CRITICAL RULE:
    # Annotation links belong to header
    header_links = annotation_links.copy()

    # All links (used for project matching)
    all_links = [l["url"] for l in text_links] + annotation_links

    emails = re.findall(EMAIL_REGEX, resume_text)
    phones = re.findall(PHONE_REGEX, resume_text)

    return {
        "contact": {
            "email": emails[0] if emails else "",
            "phone": phones[0] if phones else ""
        },
        "header_links": list(dict.fromkeys(header_links)),
        "links": list(dict.fromkeys(all_links))
    }
