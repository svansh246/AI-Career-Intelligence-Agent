CAREER_REQUIREMENTS = {

    "AI / Machine Learning": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Computer Vision",
        "Natural Language Processing",
        "Generative AI",
        "LLM",
        "RAG"
    ],

    "Data Science": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Scikit-learn",
        "Data Science",
        "Data Analysis",
        "Power BI"
    ],

    "Software Development": [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "Git",
        "GitHub",
        "SQL"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "JavaScript",
        "Bootstrap",
        "React",
        "Node.js",
        "Express.js",
        "Git",
        "GitHub"
    ],

    "Cloud / DevOps": [
        "AWS",
        "Azure",
        "Docker",
        "Git",
        "GitHub",
        "Python"
    ]
}


def analyze_skill_gap(user_skills, career_domain):

    required_skills = CAREER_REQUIREMENTS.get(
        career_domain,
        []
    )

    user_skills_lower = [
        skill.lower()
        for skill in user_skills
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in user_skills_lower:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    total_required = len(required_skills)

    if total_required > 0:

        match_percentage = round(
            (len(matched_skills) / total_required) * 100
        )

    else:

        match_percentage = 0

    return {
        "matched": matched_skills,
        "missing": missing_skills,
        "percentage": match_percentage
    }