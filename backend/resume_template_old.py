from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def find_link_for_text(text: str, links: list[str]):
    """
    Returns the first link that loosely matches the given text.
    Matching is case-insensitive substring.
    """
    text_l = text.lower().replace(" ", "")
    for url in links:
        if text_l in url.lower().replace("-", "").replace("_", ""):
            return url
    return None

def label_for_url(url: str) -> str:
    """
    Convert URL into a readable label without hardcoding platforms.
    """
    domain = url.split("//")[-1].split("/")[0].lower()
    domain = domain.replace("www.", "")

    # take first meaningful token
    label = domain.split(".")[0]

    return label.capitalize()


def render_resume(c, data):
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle("Name", parent=styles["Title"], fontSize=18)
    header_style = ParagraphStyle("Header", parent=styles["Normal"], fontSize=10)
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=11,
        spaceBefore=14,
        spaceAfter=6,
        borderBottom=1,
    )
    bullet_style = ParagraphStyle(
        "Bullet", parent=styles["Normal"], leftIndent=12
    )

    story = []

    # ---------- NAME ----------
    if data.get("name"):
        story.append(Paragraph(data["name"], name_style))

    # ---------- CURRENT ROLE ----------
    if data.get("current_role"):
        story.append(Paragraph(data["current_role"], header_style))

    # ---------- CONTACT + LINKS ----------
    ctc = data.get("contact", {})
    links = data.get("header_links", [])

    header_items = []

    if ctc.get("email"):
        header_items.append(ctc["email"])
    if ctc.get("phone"):
        header_items.append(ctc["phone"])

    # Generic link rendering (NO assumptions)
    for url in links:
        label = label_for_url(url)
        header_items.append(f"<link href='{url}'>{label}</link>")


    if header_items:
        story.append(Paragraph(" | ".join(header_items), header_style))

    story.append(Spacer(1, 12))

    # ---------- SUMMARY ----------
    if data.get("summary"):
        story.append(Paragraph("SUMMARY", section_style))
        story.append(Paragraph(data["summary"], styles["Normal"]))

    # ---------- WORK EXPERIENCE ----------
    if data.get("work_experience"):
        story.append(Paragraph("WORK EXPERIENCE", section_style))
        for exp in data["work_experience"]:
            title = " - ".join(
                filter(None, [exp.get("role"), exp.get("company")])
            )
            if title:
                story.append(Paragraph(f"<b>{title}</b>", styles["Normal"]))

            if exp.get("duration"):
                story.append(Paragraph(exp["duration"], styles["Italic"]))

            for b in exp.get("bullets", []):
                story.append(
                    ListFlowable(
                        [Paragraph(b, bullet_style)],
                        bulletType="bullet",
                    )
                )

    # ---------- PROJECTS ----------
    if data.get("projects"):
        story.append(Paragraph("PROJECTS", section_style))
        for proj in data["projects"]:
            name = proj.get("name", "")
            project_link = find_link_for_text(name, links)

            if name:
                if project_link:
                    story.append(
                        Paragraph(
                            f"<b><link href='{project_link}'>{name}</link></b>",
                            styles["Normal"]
                        )
                    )
                else:
                    story.append(
                        Paragraph(f"<b>{name}</b>", styles["Normal"])
                    )


            if proj.get("description"):
                story.append(
                    Paragraph(proj["description"], styles["Normal"])
                )

            for b in proj.get("bullets", []):
                story.append(
                    ListFlowable(
                        [Paragraph(b, bullet_style)],
                        bulletType="bullet",
                    )
                )

    # ---------- SKILLS ----------
    if data.get("skills"):
        story.append(Paragraph("SKILLS", section_style))
        for k, v in data["skills"].items():
            if v:
                story.append(
                    Paragraph(
                        f"<b>{k}:</b> {', '.join(v)}",
                        styles["Normal"],
                    )
                )

    # ---------- EDUCATION ----------
    if data.get("education"):
        story.append(Paragraph("EDUCATION", section_style))
        for edu in data["education"]:
            line = " | ".join(
                filter(
                    None,
                    [
                        edu.get("degree"),
                        edu.get("institution"),
                        edu.get("year"),
                    ],
                )
            )
            if line:
                story.append(Paragraph(line, styles["Normal"]))

    # ---------- BUILD PDF ----------
    doc = SimpleDocTemplate(
        c._filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36,
    )
    doc.build(story)
