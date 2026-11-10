WEIGHTS = {
    "Technical Skills": 30,
    "Education": 15,
    "Experience": 20,
    "Projects": 15,
    "Certifications": 10,
    "Career Alignment": 10
}


def calculate_score(value, maximum):
    """Convert a value into a percentage score."""
    if maximum <= 0:
        return 0

    return round(
        min(value / maximum, 1) * 100
    )


def evaluate_readiness(
    profile,
    skills,
    skill_gap,
    primary_domain
):
    """
    Calculate a transparent, rule-based career
    readiness score from the parsed resume.
    """

    # 1. Technical skills
    # Up to 8 detected skills receive full credit.
    technical_score = calculate_score(
        len(skills),
        8
    )

    # 2. Education
    education = profile.get(
        "education",
        []
    )

    education_score = (
        100 if education else 0
    )

    # 3. Experience
    experience = profile.get(
        "experience",
        []
    )

    experience_score = calculate_score(
        len(experience),
        2
    )

    # 4. Projects
    projects = profile.get(
        "projects",
        []
    )

    project_score = calculate_score(
        len(projects),
        3
    )

    # 5. Certifications
    certifications = profile.get(
        "certifications",
        []
    )

    certification_score = calculate_score(
        len(certifications),
        2
    )

    # 6. Career alignment
    # Based on the percentage of required skills matched.
    alignment_score = skill_gap.get(
        "percentage",
        0
    )

    category_scores = {
        "Technical Skills": technical_score,
        "Education": education_score,
        "Experience": experience_score,
        "Projects": project_score,
        "Certifications": certification_score,
        "Career Alignment": alignment_score
    }

    weighted_total = 0

    for category, weight in WEIGHTS.items():

        weighted_total += (
            category_scores[category]
            * weight
        )

    overall_score = round(
        weighted_total / 100
    )

    # Identify areas that need attention.
    improvement_areas = sorted(
        category_scores.items(),
        key=lambda item: item[1]
    )

    return {
        "overall": overall_score,
        "categories": category_scores,
        "weights": WEIGHTS,
        "improvement_areas": improvement_areas,
        "domain": primary_domain
    }


def readiness_label(score):

    if score >= 80:
        return "Strong profile coverage"

    elif score >= 60:
        return "Developing profile"

    elif score >= 40:
        return "Early-stage profile"

    return "Foundational profile"