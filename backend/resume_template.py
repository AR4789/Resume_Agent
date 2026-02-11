from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    ListFlowable, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER



# =========================
# THEME PRESETS
# =========================

THEMES = {
    "minimal": {
        "accent": colors.black,
        "muted": colors.grey,
        "name_size": 18,
        "section_size": 11,
    },
    "modern": {
        "accent": colors.HexColor("#1F3A5F"),
        "muted": colors.HexColor("#555555"),
        "name_size": 20,
        "section_size": 11,
    },
    "premium": {
        "accent": colors.HexColor("#0F4C5C"),
        "muted": colors.HexColor("#444444"),
        "name_size": 22,
        "section_size": 12,
    }
}


# =========================
# HELPERS
# =========================

def label_for_url(url: str) -> str:
    domain = url.split("//")[-1].split("/")[0].lower()
    domain = domain.replace("www.", "")
    return domain.split(".")[0].capitalize()


def find_link_for_text(text: str, links: list[str]):
    key = text.lower().replace(" ", "")
    for u in links:
        if key in u.lower().replace("-", "").replace("_", ""):
            return u
    return None


def section_divider(width=520, thickness=1.4, color=colors.lightgrey):
    table = Table(
        [[""]],
        colWidths=[width],
        rowHeights=[thickness]
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
    ]))
    return [Spacer(1, 8), table, Spacer(1, 8)]


def heading_underline(theme, width=520, thickness=1.4):
    table = Table(
        [[""]],
        colWidths=[width],
        rowHeights=[thickness]
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), theme["accent"]),
    ]))
    return [table, Spacer(1, 8)]


def section_heading(text, theme, styles):
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=theme["section_size"],
        textColor=theme["accent"],
        spaceBefore=12,
        spaceAfter=4,
    )

    return [
        Paragraph(text, section_style),
        *heading_underline(theme)
    ]


# =========================
# RENDERER
# =========================

def render_resume(c, data, design="modern", density="detailed"):
    theme = THEMES.get(design, THEMES["modern"])
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        parent=styles["Title"],
        fontSize=theme["name_size"],
        textColor=theme["accent"],
        spaceAfter=6,
    )

    header_style = ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontSize=10,
        textColor=theme["muted"],
        spaceAfter=6,
        alignment=TA_CENTER,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        leftIndent=14,
        bulletIndent=6,
        spaceBefore=2,
        spaceAfter=4 if density == "detailed" else 2,
    )

    story = []

    # ---------- HEADER ----------
    story.append(Paragraph(data.get("name", ""), name_style))


    header_items = []
    ctc = data.get("contact", {})
    header_links = data.get("header_links", [])

    if ctc.get("email"):
        header_items.append(ctc["email"])
    if ctc.get("phone"):
        header_items.append(ctc["phone"])

    for url in header_links:
        header_items.append(
            f"<link href='{url}'>{label_for_url(url)}</link>"
        )

    if header_items:
        story.append(Paragraph(" | ".join(header_items), header_style))

    # ---------- SUMMARY ----------
    if data.get("summary"):
        story.extend(section_heading("PROFESSIONAL SUMMARY", theme, styles))
        story.append(Paragraph(data["summary"], styles["Normal"]))

    # ---------- WORK EXPERIENCE ----------
    if data.get("work_experience"):
        story.extend(section_heading("WORK EXPERIENCE", theme, styles))
        for exp in data["work_experience"]:
            title = " - ".join(filter(None, [exp.get("role"), exp.get("company")]))
            if title:
                story.append(
                    Paragraph(
                        f"<b><font color='{theme['accent'].hexval()}'>{title}</font></b>",
                        styles["Normal"]
                    )
                )

            if exp.get("duration"):
                story.append(
                    Paragraph(
                        f"<font size=9 color='{theme['muted'].hexval()}'>{exp['duration']}</font>",
                        styles["Normal"]
                    )
                )

            bullets = exp.get("bullets", [])
            if density == "compact":
                bullets = bullets[:2]

            for b in bullets:
                story.append(
                    ListFlowable(
                        [Paragraph(b, bullet_style)],
                        bulletType="bullet"
                    )
                )

    # ---------- PROJECTS ----------
    if data.get("projects"):
        story.extend(section_heading("PROJECTS", theme, styles))
        all_links = data.get("links", [])

        for proj in data["projects"]:
            name = proj.get("name", "")
            link = find_link_for_text(name, all_links)

            if name:
                if link:
                    story.append(
                        Paragraph(
                            # f"<b><link href='{link}'>{name}</link></b>",
                            f"<b><a href='{link}' color='{theme['accent'].hexval()}'>{name}</a></b> "
                            f"<font size='8' color='{theme['muted'].hexval()}'>&nbsp;(Live)</font>",
                            styles["Normal"]
                        )
                    )
                else:
                    story.append(Paragraph(f"<b>{name}</b>", styles["Normal"]))

            bullets = proj.get("bullets", [])
            if density == "compact":
                bullets = bullets[:2]

            for b in bullets:
                story.append(
                    ListFlowable(
                        [Paragraph(b, bullet_style)],
                        bulletType="bullet"
                    )
                )

    # ---------- SKILLS ----------
    if data.get("skills"):
        story.extend(section_heading("SKILLS", theme, styles))

        skill_rows = []
        for k, v in data["skills"].items():
            if v:
                skill_rows.append([
                    Paragraph(f"<b>{k}</b>", styles["Normal"]),
                    Paragraph(", ".join(v), styles["Normal"])
                ])

        table = Table(skill_rows, colWidths=[120, 360])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(table)

    # ---------- EDUCATION ----------
    if data.get("education"):
        story.extend(section_heading("EDUCATION", theme, styles))
        for edu in data["education"]:
            line = " | ".join(filter(None, [
                edu.get("degree"),
                edu.get("institution"),
                edu.get("year")
            ]))
            if line:
                story.append(Paragraph(line, styles["Normal"]))

    # ---------- BUILD ----------
    doc = SimpleDocTemplate(
        c._filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36,
    )
    doc.build(story)
