from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def generate_pdf_report(analysis):
    """
    Generate a professional PDF resume analysis report.
    Returns PDF data as bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=5,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
    )

    story = []

    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    user_name = analysis.get(
        "user_name",
        "Not provided"
    )

    resume_name = analysis.get(
        "resume_name",
        "Not provided"
    )

    target_domain = analysis.get(
        "target_domain",
        "Not specified"
    )

    score = analysis.get(
        "readiness_score",
        0
    )

    skills = analysis.get(
        "skills",
        []
    )

    profile = analysis.get(
        "profile",
        {}
    )

    strengths = profile.get(
        "strengths",
        []
    )

    weaknesses = profile.get(
        "weaknesses",
        []
    )

    recommendations = profile.get(
        "recommendations",
        []
    )

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "AI Career Assistant",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Resume & Career Intelligence Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            f"Generated on "
            f"{datetime.now().strftime('%d %B %Y, %H:%M')}",
            subtitle_style
        )
    )

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "1. Candidate Information",
            heading_style
        )
    )

    candidate_data = [
        ["Name", str(user_name)],
        ["Resume", str(resume_name)],
        ["Target Domain", str(target_domain)],
    ]

    table = Table(
        candidate_data,
        colWidths=[
            45 * mm,
            125 * mm
        ],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(table)

    # -----------------------------------------------------
    # READINESS SCORE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "2. Career Readiness Score",
            heading_style
        )
    )

    score_table = Table(
        [
            [
                Paragraph(
                    f"<b>{score}/100</b>",
                    ParagraphStyle(
                        "Score",
                        parent=body_style,
                        fontSize=24,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ],
        colWidths=[170 * mm],
    )

    score_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )

    story.append(score_table)

    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "3. Detected Technical Skills",
            heading_style
        )
    )

    if skills:

        skill_text = ", ".join(
            str(skill)
            for skill in skills
        )

        story.append(
            Paragraph(
                skill_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "No technical skills were detected.",
                body_style
            )
        )

    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "4. Profile Analysis",
            heading_style
        )
    )

    profile_items = [
        (
            "Resume Word Count",
            profile.get(
                "resume_length",
                "Not available"
            ),
        ),
        (
            "Skills Detected",
            profile.get(
                "skills_detected",
                len(skills)
            ),
        ),
        (
            "Education Detected",
            "Yes"
            if profile.get(
                "education_detected",
                False
            )
            else "No",
        ),
        (
            "Experience Detected",
            "Yes"
            if profile.get(
                "experience_detected",
                False
            )
            else "No",
        ),
        (
            "Projects Detected",
            "Yes"
            if profile.get(
                "projects_detected",
                False
            )
            else "No",
        ),
        (
            "GitHub Detected",
            "Yes"
            if profile.get(
                "github_detected",
                False
            )
            else "No",
        ),
        (
            "LinkedIn Detected",
            "Yes"
            if profile.get(
                "linkedin_detected",
                False
            )
            else "No",
        ),
    ]

    profile_data = [
        ["Metric", "Result"]
    ]

    for key, value in profile_items:

        profile_data.append(
            [
                str(key),
                str(value)
            ]
        )

    profile_table = Table(
        profile_data,
        colWidths=[
            85 * mm,
            85 * mm
        ],
    )

    profile_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(profile_table)

    # -----------------------------------------------------
    # STRENGTHS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "5. Strengths",
            heading_style
        )
    )

    if strengths:

        for item in strengths:

            story.append(
                Paragraph(
                    f"• {item}",
                    body_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No strengths recorded.",
                body_style
            )
        )

    # -----------------------------------------------------
    # AREAS FOR IMPROVEMENT
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "6. Areas for Improvement",
            heading_style
        )
    )

    if weaknesses:

        for item in weaknesses:

            story.append(
                Paragraph(
                    f"• {item}",
                    body_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No major improvement areas recorded.",
                body_style
            )
        )

    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "7. Career Recommendations",
            heading_style
        )
    )

    if recommendations:

        for item in recommendations:

            story.append(
                Paragraph(
                    f"• {item}",
                    body_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No recommendations available.",
                body_style
            )
        )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    story.append(
        Spacer(
            1,
            20
        )
    )

    story.append(
        Paragraph(
            "Generated by AI Career Assistant",
            small_style
        )
    )

    # -----------------------------------------------------
    # BUILD PDF
    # -----------------------------------------------------

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()