
def normalize_skills(skills):
    """Normalize skills for case-insensitive comparison."""
    if not isinstance(skills, (list, tuple, set)):
        return set()

    return {
        str(skill).strip().lower()
        for skill in skills
        if str(skill).strip()
    }


def calculate_percentage(matched, total):
    """Calculate percentage safely."""
    if isinstance(total, (list, tuple, set)):
        total = len(total)

    if not total:
        return 0

    return round(len(matched) / total * 100)


def match_resume_to_job(
    profile,
    resume_skills,
    job_result
):
    """
    Calculate a transparent resume-to-job match.

    Weights:
    Technical skills: 50%
    Experience: 20%
    Projects: 20%
    Education: 10%
    """

    weights = {
        "Technical Skills": 50,
        "Experience": 20,
        "Projects": 20,
        "Education": 10
    }

    if not isinstance(profile, dict):
        profile = {}

    if not isinstance(job_result, dict):
        job_result = {}

    # --------------------------------------------------------
    # TECHNICAL SKILLS
    # --------------------------------------------------------

    job_skills = job_result.get("job_skills", [])

    if not isinstance(job_skills, (list, tuple, set)):
        job_skills = []

    job_skills = [
        str(skill).strip()
        for skill in job_skills
        if str(skill).strip()
    ]

    resume_lookup = normalize_skills(resume_skills)

    matched_skills = [
        skill
        for skill in job_skills
        if skill.lower() in resume_lookup
    ]

    missing_skills = [
        skill
        for skill in job_skills
        if skill.lower() not in resume_lookup
    ]

    technical_score = calculate_percentage(
        matched_skills,
        len(job_skills)
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    experiences = profile.get("experience", [])

    if not isinstance(experiences, list):
        experiences = []

    experience_score = 100 if experiences else 0

    # --------------------------------------------------------
    # PROJECTS
    # --------------------------------------------------------

    projects = profile.get("projects", [])

    if not isinstance(projects, list):
        projects = []

    project_text_parts = []

    for project in projects:
        if isinstance(project, dict):
            name = project.get("name", "")
            description = project.get("description", "")
            project_text_parts.append(
                str(name) + " " + str(description)
            )
        else:
            project_text_parts.append(str(project))

    project_text = " ".join(
        project_text_parts
    ).lower()

    project_skill_matches = [
        skill
        for skill in job_skills
        if skill.lower() in project_text
    ]

    if job_skills:
        project_score = calculate_percentage(
            project_skill_matches,
            len(job_skills)
        )
    else:
        project_score = 100 if projects else 0

    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    education = profile.get("education", [])

    if not isinstance(education, list):
        education = []

    education_score = 100 if education else 0

    # --------------------------------------------------------
    # OVERALL WEIGHTED SCORE
    # --------------------------------------------------------

    category_scores = {
        "Technical Skills": technical_score,
        "Experience": experience_score,
        "Projects": project_score,
        "Education": education_score
    }

    overall_score = round(
        sum(
            category_scores[name] * weight
            for name, weight in weights.items()
        ) / 100
    )

    # --------------------------------------------------------
    # MATCH EXPLANATION
    # --------------------------------------------------------

    strengths = []
    improvement_areas = []

    if matched_skills:
        strengths.append(
            "Your resume contains "
            + ", ".join(matched_skills)
            + "."
        )

    if experiences:
        strengths.append(
            "Your resume includes work experience."
        )
    else:
        improvement_areas.append(
            "Add relevant experience or clearly describe "
            "practical training, if applicable."
        )

    if project_skill_matches:
        strengths.append(
            "Your project descriptions mention "
            + ", ".join(project_skill_matches)
            + "."
        )

    if missing_skills:
        improvement_areas.append(
            "Review these job skills that were not detected "
            "in your resume: "
            + ", ".join(missing_skills)
            + "."
        )

    if not projects:
        improvement_areas.append(
            "Add relevant projects if you have completed them."
        )

    if not education:
        improvement_areas.append(
            "Add your education details if relevant."
        )

    if not job_skills:
        improvement_areas.append(
            "The analyzer found no predefined technical skills "
            "in this job description. Review the description "
            "manually."
        )

    return {
        "overall_score": overall_score,
        "category_scores": category_scores,
        "weights": weights,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "project_skill_matches": project_skill_matches,
        "strengths": strengths,
        "improvement_areas": improvement_areas
    }