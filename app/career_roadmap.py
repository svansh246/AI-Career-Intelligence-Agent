ROADMAPS = {

    "AI / Machine Learning": [
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "Machine Learning",
        "Scikit-learn",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Natural Language Processing",
        "Computer Vision",
        "Generative AI",
        "LLM",
        "RAG",
        "AI Project Development",
        "AI Application Deployment"
    ],

    "Data Science": [
        "Python",
        "SQL",
        "NumPy",
        "Pandas",
        "Statistics",
        "Data Visualization",
        "Scikit-learn",
        "Machine Learning",
        "Power BI",
        "Tableau",
        "Data Science Projects",
        "Industry Portfolio"
    ],

    "Software Development": [
        "Programming Fundamentals",
        "Data Structures",
        "Algorithms",
        "Python",
        "Java",
        "C++",
        "Git",
        "GitHub",
        "SQL",
        "Databases",
        "Backend Development",
        "REST APIs",
        "Full Stack Development",
        "Software Development Projects"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "JavaScript",
        "Responsive Web Design",
        "React",
        "Node.js",
        "Express.js",
        "Databases",
        "Git",
        "GitHub",
        "Full Stack Development",
        "Web Application Deployment"
    ],

    "Cloud / DevOps": [
        "Linux",
        "Networking",
        "Git",
        "GitHub",
        "AWS",
        "Azure",
        "Docker",
        "CI/CD",
        "Infrastructure",
        "Cloud Security",
        "Cloud Application Deployment",
        "DevOps Projects"
    ]
}


def generate_roadmap(career_domain, missing_skills):

    roadmap = ROADMAPS.get(
        career_domain,
        []
    )

    if not roadmap:
        return []

    missing_lower = [
        skill.lower()
        for skill in missing_skills
    ]

    priority_steps = []
    normal_steps = []

    for step in roadmap:

        step_lower = step.lower()

        is_missing = any(
            missing_skill in step_lower
            or step_lower in missing_skill
            for missing_skill in missing_lower
        )

        if is_missing:

            priority_steps.append(step)

        else:

            normal_steps.append(step)

    return priority_steps + normal_steps