import re


SKILLS = [

    # -----------------------------
    # Programming Languages
    # -----------------------------

    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "TypeScript",
    "SQL",
    "R",

    # -----------------------------
    # Data Science
    # -----------------------------

    "Data Science",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "Statistics",
    "Data Visualization",

    # -----------------------------
    # Machine Learning
    # -----------------------------

    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",

    # -----------------------------
    # Artificial Intelligence
    # -----------------------------

    "Artificial Intelligence",
    "Generative AI",
    "Large Language Models",
    "LLM",
    "RAG",
    "LangChain",
    "Prompt Engineering",

    # -----------------------------
    # AI Frameworks
    # -----------------------------

    "TensorFlow",
    "PyTorch",
    "Keras",

    # -----------------------------
    # Databases
    # -----------------------------

    "MySQL",
    "PostgreSQL",
    "MongoDB",

    # -----------------------------
    # Cloud / DevOps
    # -----------------------------

    "AWS",
    "Azure",
    "Docker",
    "Linux",
    "Git",
    "GitHub",
    "CI/CD",

    # -----------------------------
    # Visualization / BI
    # -----------------------------

    "Power BI",
    "Tableau",

    # -----------------------------
    # Web Development
    # -----------------------------

    "HTML",
    "CSS",
    "Bootstrap",
    "React",
    "Node.js",
    "Express.js",

    # -----------------------------
    # Other Technical Skills
    # -----------------------------

    "Data Structures",
    "Algorithms",
    "REST API",
    "REST APIs",
    "API",
    "Excel"
]


def skill_pattern(skill):

    escaped_skill = re.escape(skill)

    # Special handling for single-letter programming language
    if skill == "C":

        return re.compile(
            r"(?<![A-Za-z])C(?![A-Za-z+#])",
            re.IGNORECASE
        )

    return re.compile(
        r"(?<![A-Za-z0-9])"
        + escaped_skill
        + r"(?![A-Za-z0-9])",
        re.IGNORECASE
    )


def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        pattern = skill_pattern(skill)

        if pattern.search(text):

            found_skills.append(skill)

    return found_skills