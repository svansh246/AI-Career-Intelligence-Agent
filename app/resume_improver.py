
import re


SECTION_KEYWORDS = {
    "Contact Information": [
        "email", "phone", "mobile", "linkedin", "github"
    ],
    "Professional Summary": [
        "summary", "objective", "profile"
    ],
    "Education": [
        "education", "academic", "qualification"
    ],
    "Technical Skills": [
        "skills", "technical skills", "technologies"
    ],
    "Experience": [
        "experience", "internship", "employment", "work history"
    ],
    "Projects": [
        "projects", "academic projects", "personal projects"
    ],
    "Certifications": [
        "certifications", "certificates", "courses"
    ]
}


def check_sections(resume_text):
    """Check which common resume sections appear in the text."""
    text = resume_text.lower()
    results = {}

    for section, keywords in SECTION_KEYWORDS.items():
        found = any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            )
            for keyword in keywords
        )
        results[section] = found

    return results


def check_contact_information(profile, resume_text):
    """Check basic contact details."""
    contact = profile.get("contact", {})

    email = contact.get("email")
    phone = contact.get("phone")

    if not email:
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            resume_text
        )
        email = email_match.group(0) if email_match else None

    if not phone:
        phone_match = re.search(
            r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
            resume_text
        )
        phone = phone_match.group(0) if phone_match else None

    return {
        "email_found": bool(email),
        "phone_found": bool(phone)
    }


def check_summary(profile, resume_text):
    """Review the professional summary."""
    summary = profile.get("profile", "")

    if not summary or summary.lower() in [
        "not available", "none", "not detected"
    ]:
        return {
            "status": "Missing",
            "suggestion": (
                "Add a short professional summary describing "
                "your background, key skills, and career direction."
            )
        }

    word_count = len(summary.split())

    if word_count < 25:
        return {
            "status": "Needs improvement",
            "suggestion": (
                "Expand your summary with your specialization, "
                "relevant skills, and the type of role you are pursuing."
            )
        }

    if word_count > 100:
        return {
            "status": "Needs improvement",
            "suggestion": (
                "Shorten your summary. Aim for a concise introduction "
                "that highlights your most relevant qualifications."
            )
        }

    return {
        "status": "Present",
        "suggestion": (
            "Check that your summary is specific to your target role "
            "and focuses on relevant qualifications."
        )
    }


def check_experience(profile, resume_text):
    """Check experience content and look for measurable evidence."""
    experience = profile.get("experience", [])

    if not experience:
        return {
            "status": "Not detected",
            "suggestion": (
                "If you have internships, employment, volunteering, "
                "or relevant practical experience, add it with your "
                "role, organization, dates, and contributions."
            )
        }

    measurable_pattern = re.compile(
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:%|percent|users|customers|projects|hours|days|weeks|months)\b",
        re.IGNORECASE
    )

    has_metrics = bool(measurable_pattern.search(resume_text))

    if not has_metrics:
        return {
            "status": "Experience detected",
            "suggestion": (
                "Where accurate, add measurable outcomes to your "
                "experience bullets, such as time saved, records "
                "processed, or project results."
            )
        }

    return {
        "status": "Experience detected",
        "suggestion": (
            "Make sure each experience entry explains your actions, "
            "tools used, and outcomes."
        )
    }


def check_projects(profile):
    """Review project descriptions."""
    projects = profile.get("projects", [])

    if not projects:
        return {
            "status": "Not detected",
            "suggestion": (
                "Add relevant academic or personal projects. Explain "
                "the problem, your contribution, tools, and outcome."
            )
        }

    weak_descriptions = []

    for project in projects:
        if isinstance(project, dict):
            name = project.get("name", "Unnamed project")
            description = project.get("description", "")
        else:
            name = str(project)
            description = ""

        if len(description.split()) < 10:
            weak_descriptions.append(name)

    if weak_descriptions:
        return {
            "status": "Projects detected",
            "suggestion": (
                "Expand the descriptions for: "
                + ", ".join(weak_descriptions)
                + ". Include the purpose, technologies, and your role."
            )
        }

    return {
        "status": "Projects detected",
        "suggestion": (
            "Check that each project clearly communicates your "
            "individual contribution and what you achieved."
        )
    }


def check_skills(profile, skills, target_domain=None):
    """Review whether technical skills are listed."""
    if not skills:
        return {
            "status": "No skills detected",
            "suggestion": (
                "Add a clearly labeled technical skills section. "
                "List tools and technologies you can genuinely use."
            )
        }

    suggestion = (
        "Group related skills into categories and prioritize "
        "those relevant to your target role."
    )

    if target_domain:
        suggestion += (
            f" Review the skills expected for {target_domain} "
            "and include relevant ones only when you have them."
        )

    return {
        "status": "Skills detected",
        "suggestion": suggestion
    }


def generate_resume_review(
    resume_text,
    profile,
    skills,
    target_domain=None
):
    """Generate a rule-based resume review report."""
    if not isinstance(resume_text, str):
        resume_text = ""

    if not isinstance(profile, dict):
        profile = {}

    if not isinstance(skills, list):
        skills = []

    sections = check_sections(resume_text)
    contact = check_contact_information(
        profile,
        resume_text
    )

    summary = check_summary(
        profile,
        resume_text
    )

    experience = check_experience(
        profile,
        resume_text
    )

    projects = check_projects(profile)

    skill_review = check_skills(
        profile,
        skills,
        target_domain
    )

    checks = {
        "Contact Information": {
            "status": (
                "Present"
                if contact["email_found"] and contact["phone_found"]
                else "Incomplete"
            ),
            "suggestion": (
                "Ensure your email and phone number are correct "
                "and easy to find."
                if contact["email_found"] and contact["phone_found"]
                else "Check that your resume includes a professional "
                     "email address and a reachable phone number."
            )
        },
        "Professional Summary": summary,
        "Education": {
            "status": (
                "Present"
                if sections["Education"]
                else "Not detected"
            ),
            "suggestion": (
                "Include your degree, institution, and graduation "
                "details. Add relevant coursework if useful."
            )
        },
        "Technical Skills": skill_review,
        "Experience": experience,
        "Projects": projects,
        "Certifications": {
            "status": (
                "Present"
                if sections["Certifications"]
                else "Not detected"
            ),
            "suggestion": (
                "Include relevant certifications with their "
                "issuing organization and completion date."
            )
        }
    }

    present_count = sum(
        1 for item in checks.values()
        if item["status"] in [
            "Present",
            "Experience detected",
            "Projects detected",
            "Skills detected"
        ]
    )

    total = len(checks)
    completeness = round(
        present_count / total * 100
    ) if total else 0

    priorities = []

    for section, result in checks.items():
        if result["status"] in [
            "Missing",
            "Not detected",
            "Incomplete",
            "No skills detected"
        ]:
            priorities.append({
                "priority": "High",
                "section": section,
                "suggestion": result["suggestion"]
            })
        elif result["status"] == "Needs improvement":
            priorities.append({
                "priority": "Medium",
                "section": section,
                "suggestion": result["suggestion"]
            })

    return {
        "completeness_indicator": completeness,
        "checks": checks,
        "priorities": priorities,
        "target_domain": target_domain,
        "note": (
            "This is a basic rule-based review. It checks common "
            "resume elements, not actual ATS compatibility or "
            "the quality of every claim."
        )
    }