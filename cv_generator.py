"""
cv_generator.py  —  Generate a professional PDF CV from structured text.
Style matches the clean, ATS-optimised CV format used by HireReady AI.
"""

import re
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Colour palette ──────────────────────────────────────────────────────────
C_HEADING   = HexColor("#1a1a2e")   # dark navy  – section headings
C_ACCENT    = HexColor("#4a4e69")   # muted slate – thin rule + role line
C_BODY      = HexColor("#2d2d2d")   # near-black  – body text
C_LIGHT     = HexColor("#555555")   # grey        – dates / metadata
C_LINK      = HexColor("#2563eb")   # blue        – contact links
C_RULE      = HexColor("#4a4e69")   # rule colour
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


# ── Style definitions ────────────────────────────────────────────────────────
def make_styles():
    return {
        "name": ParagraphStyle(
            "name",
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=C_HEADING,
            spaceAfter=1 * mm,
            alignment=TA_CENTER,
            leading=26,
        ),
        "tagline": ParagraphStyle(
            "tagline",
            fontName="Helvetica",
            fontSize=10,
            textColor=C_ACCENT,
            spaceAfter=2 * mm,
            alignment=TA_CENTER,
            leading=14,
        ),
        "contact": ParagraphStyle(
            "contact",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=C_LIGHT,
            spaceAfter=4 * mm,
            alignment=TA_CENTER,
            leading=13,
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=C_HEADING,
            spaceBefore=4 * mm,
            spaceAfter=1 * mm,
            leading=14,
            textTransform="uppercase",
        ),
        "job_title": ParagraphStyle(
            "job_title",
            fontName="Helvetica-Bold",
            fontSize=9.5,
            textColor=C_BODY,
            spaceAfter=0.5 * mm,
            leading=13,
        ),
        "job_meta": ParagraphStyle(
            "job_meta",
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            textColor=C_LIGHT,
            spaceAfter=1 * mm,
            leading=12,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=8.8,
            textColor=C_BODY,
            leftIndent=10,
            spaceAfter=1.2 * mm,
            leading=13,
            bulletIndent=2,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=8.8,
            textColor=C_BODY,
            spaceAfter=1.5 * mm,
            leading=13,
        ),
        "skills_label": ParagraphStyle(
            "skills_label",
            fontName="Helvetica-Bold",
            fontSize=8.8,
            textColor=C_BODY,
            leading=13,
        ),
        "skills_value": ParagraphStyle(
            "skills_value",
            fontName="Helvetica",
            fontSize=8.8,
            textColor=C_BODY,
            leading=13,
        ),
    }


def _rule():
    return HRFlowable(
        width="100%",
        thickness=0.6,
        color=C_RULE,
        spaceAfter=2 * mm,
        spaceBefore=0,
    )


def _section(styles, title):
    return [
        Paragraph(title.upper(), styles["section_heading"]),
        _rule(),
    ]


def _bullets(styles, items):
    out = []
    for item in items:
        text = item.lstrip("•■-– ").strip()
        if text:
            out.append(Paragraph(f"&#8226; &nbsp;{text}", styles["bullet"]))
    return out


# ── Main builder ─────────────────────────────────────────────────────────────
def build_cv_pdf(cv_data: dict) -> bytes:
    """
    cv_data keys (all optional except 'name'):
      name, tagline, phone, email, linkedin, github, portfolio, location,
      summary,
      experience: [{title, company, date, location, bullets:[str]}],
      projects:   [{name, tech, date, bullets:[str]}],
      education:  [{degree, institution, date, location, bullets:[str]}],
      certifications: [str],
      skills: {Category: "val1, val2, ..."}
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )
    S = make_styles()
    story = []

    # ── Header ───────────────────────────────────────────────────────────────
    story.append(Paragraph(cv_data.get("name", "Your Name").upper(), S["name"]))

    if cv_data.get("tagline"):
        story.append(Paragraph(cv_data["tagline"], S["tagline"]))

    contact_parts = []
    for key in ("phone", "email", "linkedin", "github", "portfolio", "location"):
        val = cv_data.get(key, "").strip()
        if val:
            contact_parts.append(val)
    if contact_parts:
        story.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_parts), S["contact"]))

    story.append(_rule())

    # ── Summary ──────────────────────────────────────────────────────────────
    if cv_data.get("summary"):
        story += _section(S, "Professional Summary")
        story.append(Paragraph(cv_data["summary"], S["body"]))

    # ── Technical Skills ─────────────────────────────────────────────────────
    if cv_data.get("skills"):
        story += _section(S, "Technical Skills")
        for label, value in cv_data["skills"].items():
            row_data = [[
                Paragraph(f"{label}:", S["skills_label"]),
                Paragraph(value, S["skills_value"]),
            ]]
            t = Table(row_data, colWidths=[38 * mm, None])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(t)

    # ── Work Experience ───────────────────────────────────────────────────────
    if cv_data.get("experience"):
        story += _section(S, "Work Experience")
        for job in cv_data["experience"]:
            # Title + date on same line
            title_date = [[
                Paragraph(f"{job.get('title','')} &nbsp;—&nbsp; {job.get('company','')}", S["job_title"]),
                Paragraph(job.get("date", ""), S["job_meta"]),
            ]]
            t = Table(title_date, colWidths=[None, 38 * mm])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]))
            story.append(t)
            if job.get("location"):
                story.append(Paragraph(job["location"], S["job_meta"]))
            story += _bullets(S, job.get("bullets", []))
            story.append(Spacer(1, 1.5 * mm))

    # ── Projects ─────────────────────────────────────────────────────────────
    if cv_data.get("projects"):
        story += _section(S, "Projects")
        for proj in cv_data["projects"]:
            name = proj.get("name", "")
            tech = proj.get("tech", "")
            date = proj.get("date", "")
            header_left = f"<b>{name}</b>"
            if tech:
                header_left += f" &nbsp;<font color='#555555' size='8'>{tech}</font>"
            row = [[
                Paragraph(header_left, S["job_title"]),
                Paragraph(date, S["job_meta"]),
            ]]
            t = Table(row, colWidths=[None, 28 * mm])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]))
            story.append(t)
            story += _bullets(S, proj.get("bullets", []))
            story.append(Spacer(1, 1.5 * mm))

    # ── Education ────────────────────────────────────────────────────────────
    if cv_data.get("education"):
        story += _section(S, "Education")
        for edu in cv_data["education"]:
            row = [[
                Paragraph(f"<b>{edu.get('degree','')}</b> &nbsp;—&nbsp; {edu.get('institution','')}", S["job_title"]),
                Paragraph(edu.get("date", ""), S["job_meta"]),
            ]]
            t = Table(row, colWidths=[None, 38 * mm])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]))
            story.append(t)
            if edu.get("location"):
                story.append(Paragraph(edu["location"], S["job_meta"]))
            story += _bullets(S, edu.get("bullets", []))
            story.append(Spacer(1, 1.5 * mm))

    # ── Certifications ────────────────────────────────────────────────────────
    if cv_data.get("certifications"):
        story += _section(S, "Certifications & Achievements")
        for cert in cv_data["certifications"]:
            story.append(Paragraph(f"&#8226; &nbsp;{cert}", S["bullet"]))

    doc.build(story)
    return buf.getvalue()


# ── Parse plain-text resume → cv_data dict ───────────────────────────────────
def parse_resume_to_cv_data(text: str, improved_text: str = None) -> dict:
    """
    Light-weight heuristic parser.  Works well on the ATS-style plain text
    that pdf.js / mammoth extract.  Falls back gracefully when sections are absent.
    """
    src = improved_text if improved_text else text
    lines = [l.rstrip() for l in src.splitlines()]

    cv = {}

    # ── Name: first non-empty line ────────────────────────────────────────
    for line in lines:
        if line.strip():
            cv["name"] = line.strip()
            break

    # ── Contact line: look for email / phone ─────────────────────────────
    for line in lines[:8]:
        if "@" in line or re.search(r'\+?\d[\d\s\-]{8,}', line):
            parts = [p.strip() for p in re.split(r'\s*[|·•]\s*', line) if p.strip()]
            for p in parts:
                if "@" in p:           cv["email"] = p
                elif re.match(r'^\+?\d', p): cv["phone"] = p
                elif "linkedin" in p.lower(): cv["linkedin"] = p
                elif "github" in p.lower():   cv["github"] = p
                elif "portfolio" in p.lower() or "port" in p.lower(): cv["portfolio"] = p
                elif re.search(r'[A-Z][a-z]+,\s*[A-Z]', p): cv["location"] = p
            break

    # ── Section splitter ─────────────────────────────────────────────────
    SECTION_KEYWORDS = {
        "summary":          ["summary", "objective", "professional summary", "profile"],
        "experience":       ["work experience", "experience", "employment"],
        "projects":         ["projects", "project"],
        "education":        ["education"],
        "certifications":   ["certifications", "achievements", "certifications & achievements"],
        "skills":           ["technical skills", "skills", "technologies"],
    }

    def detect_section(line):
        l = line.strip().lower().rstrip(":")
        for key, kws in SECTION_KEYWORDS.items():
            if l in kws:
                return key
        return None

    sections_raw = {}
    current = None
    for line in lines[1:]:
        sec = detect_section(line)
        if sec:
            current = sec
            sections_raw[current] = []
        elif current:
            sections_raw[current].append(line)

    # ── Summary ──────────────────────────────────────────────────────────
    if "summary" in sections_raw:
        paras = " ".join(l for l in sections_raw["summary"] if l.strip())
        cv["summary"] = paras.strip()

    # ── Tagline: second non-empty line if short ───────────────────────────
    non_empty = [l for l in lines if l.strip()]
    if len(non_empty) > 1:
        candidate = non_empty[1].strip()
        if len(candidate) < 60 and not "@" in candidate:
            cv["tagline"] = candidate

    # ── Skills ───────────────────────────────────────────────────────────
    if "skills" in sections_raw:
        skills = {}
        for line in sections_raw["skills"]:
            if ":" in line:
                label, _, val = line.partition(":")
                skills[label.strip()] = val.strip()
        if skills:
            cv["skills"] = skills

    # ── Experience ───────────────────────────────────────────────────────
    def parse_entries(raw_lines):
        """Split raw section lines into entry blocks."""
        entries = []
        current_entry = None
        date_re = re.compile(
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|'
            r'\d{4}|Present|Current|Remote|–|-)',
            re.IGNORECASE
        )
        bullet_re = re.compile(r'^[•■\-–*]')

        for line in raw_lines:
            stripped = line.strip()
            if not stripped:
                continue
            is_bullet = bool(bullet_re.match(stripped))
            looks_like_header = (
                not is_bullet
                and len(stripped) > 4
                and stripped[0].isupper()
                and not stripped.startswith("Relevant")
            )
            if looks_like_header and not is_bullet:
                # New entry
                current_entry = {"header": stripped, "bullets": [], "meta": ""}
                entries.append(current_entry)
            elif is_bullet and current_entry is not None:
                current_entry["bullets"].append(stripped)
            elif current_entry is not None and date_re.search(stripped):
                current_entry["meta"] = stripped
        return entries

    if "experience" in sections_raw:
        jobs = []
        for entry in parse_entries(sections_raw["experience"]):
            hdr = entry["header"]
            # Try "Title  Company  Date" or "Title — Company"
            parts = re.split(r'\s{2,}|–|—', hdr)
            title = parts[0].strip() if parts else hdr
            company = parts[1].strip() if len(parts) > 1 else ""
            date = entry["meta"] or (parts[2].strip() if len(parts) > 2 else "")
            jobs.append({
                "title": title,
                "company": company,
                "date": date,
                "bullets": entry["bullets"],
            })
        if jobs:
            cv["experience"] = jobs

    # ── Projects ─────────────────────────────────────────────────────────
    if "projects" in sections_raw:
        projs = []
        for entry in parse_entries(sections_raw["projects"]):
            hdr = entry["header"]
            # "Name | Tech  Date" or "Name — Tech  Date"
            tech = ""
            name = hdr
            date = entry["meta"]
            tech_match = re.search(r'[|·]\s*(.+)', hdr)
            if tech_match:
                tech = tech_match.group(1).strip()
                name = hdr[:tech_match.start()].strip()
            elif re.search(r'\|\s*\w', hdr):
                parts = hdr.split("|", 1)
                name = parts[0].strip()
                tech = parts[1].strip()
            projs.append({
                "name": name,
                "tech": tech,
                "date": date,
                "bullets": entry["bullets"],
            })
        if projs:
            cv["projects"] = projs

    # ── Education ────────────────────────────────────────────────────────
    if "education" in sections_raw:
        edus = []
        for entry in parse_entries(sections_raw["education"]):
            hdr = entry["header"]
            parts = re.split(r'\s{2,}|–|—', hdr)
            institution = parts[0].strip()
            degree = parts[1].strip() if len(parts) > 1 else ""
            date = entry["meta"] or (parts[2].strip() if len(parts) > 2 else "")
            edus.append({
                "degree": degree or institution,
                "institution": institution if degree else "",
                "date": date,
                "bullets": entry["bullets"],
            })
        if edus:
            cv["education"] = edus

    # ── Certifications ───────────────────────────────────────────────────
    if "certifications" in sections_raw:
        certs = []
        for line in sections_raw["certifications"]:
            stripped = line.strip().lstrip("•■-– ").strip()
            if stripped:
                certs.append(stripped)
        if certs:
            cv["certifications"] = certs

    return cv
