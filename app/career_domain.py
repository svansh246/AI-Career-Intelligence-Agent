DOMAIN_SKILLS = {
    "AI / Machine Learning": [
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Computer Vision",
        "Natural Language Processing",
        "NLP",
        "Generative AI",
        "LLM",
        "RAG"
    ],

    "Data Science": [
        "Data Science",
        "Data Analysis",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Scikit-learn",
        "SQL",
        "Power BI",
        "Tableau"
    ],

    "Software Development": [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "TypeScript",
        "Git",
        "GitHub"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "Bootstrap",
        "JavaScript",
        "React",
        "Node.js",
        "Express.js"
    ],

    "Cloud / DevOps": [
        "AWS",
        "Azure",
        "Docker",
        "Git",
        "GitHub"
    ]
}


def detect_career_domain(skills):

    scores = {}

    for domain, domain_skills in DOMAIN_SKILLS.items():

        score = 0

        for skill in skills:

            if skill.lower() in [
                item.lower() for item in domain_skills
            ]:
                score += 1

        scores[domain] = score

    sorted_domains = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_domains