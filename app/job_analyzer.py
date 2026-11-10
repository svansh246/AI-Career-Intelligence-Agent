
import re

from skills_database import SKILLS


def extract_job_skills(text):
    """Find known technical skills in a job description."""

    found = []
    text_lower = text.lower()

    for skill in SKILLS:
        escaped = re.escape(skill)

        if skill == "C":
            pattern = r"(?<![A-Za-z])C(?![A-Za-z+#])"
        else:
            pattern = (
                r"(?<![A-Za-z0-9])"
                + escaped
                + r"(?![A-Za-z0-9])"
            )

        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)

    return found


def extract_job_sections(text):
    """Identify common requirement wording."""

    lines = text.splitlines()

    required = []
    preferred = []

    preferred_words = [
        "preferred",
        "nice to have",
        "bonus",
        "desirable",
        "plus"
    ]

    required_words = [
        "required",
        "must have",
        "minimum qualifications",
        "you will need",
        "basic qualifications"
    ]

    for line in lines:
        clean = line.strip()

        if not clean:
            continue

        lower = clean.lower()

        if any(word in lower for word in preferred_words):
            preferred.append(clean)

        elif any(word in lower for word in required_words):
            required.append(clean)

    return {
        "required_lines": required,
        "preferred_lines": preferred
    }


def analyze_job_description(
    job_text,
    resume_skills
):
    """Compare resume skills with skills found in a job ad."""

    job_skills = extract_job_skills(job_text)

    resume_lookup = {
        skill.lower(): skill
        for skill in resume_skills
    }

    matched = []
    missing = []

    for skill in job_skills:
        if skill.lower() in resume_lookup:
            matched.append(skill)
        else:
            missing.append(skill)

    if job_skills:
        match_percentage = round(
            len(matched) / len(job_skills) * 100
        )
    else:
        match_percentage = 0

    sections = extract_job_sections(job_text)

    return {
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_percentage,
        "required_lines": sections["required_lines"],
        "preferred_lines": sections["preferred_lines"]
    }