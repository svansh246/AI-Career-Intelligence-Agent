CAREER_RECOMMENDATIONS = {
    "AI / Machine Learning": {
        "roles": [
            "AI Engineer",
            "Machine Learning Engineer",
            "Deep Learning Engineer",
            "Generative AI Engineer"
        ],
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "PyTorch",
            "TensorFlow",
            "NLP",
            "Computer Vision",
            "Generative AI",
            "LLM",
            "RAG"
        ]
    },

    "Data Science": {
        "roles": [
            "Data Scientist",
            "Data Analyst",
            "Machine Learning Analyst",
            "Business Intelligence Analyst"
        ],
        "skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "Statistics",
            "Machine Learning",
            "Power BI",
            "Data Visualization"
        ]
    },

    "Software Development": {
        "roles": [
            "Software Engineer",
            "Python Developer",
            "Backend Developer",
            "Full Stack Developer"
        ],
        "skills": [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "SQL",
            "Git",
            "GitHub",
            "Data Structures",
            "Algorithms"
        ]
    },

    "Web Development": {
        "roles": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer"
        ],
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express.js",
            "Git",
            "GitHub"
        ]
    },

    "Cloud / DevOps": {
        "roles": [
            "Cloud Engineer",
            "DevOps Engineer",
            "Cloud Developer"
        ],
        "skills": [
            "AWS",
            "Azure",
            "Docker",
            "Git",
            "GitHub",
            "Linux",
            "Python",
            "CI/CD"
        ]
    }
}


def get_career_recommendations(career_domain):

    return CAREER_RECOMMENDATIONS.get(
        career_domain,
        {
            "roles": [],
            "skills": []
        }
    )