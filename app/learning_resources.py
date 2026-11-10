
RESOURCE_LIBRARY = {
    "python": [
        {
            "name": "Python Official Tutorial",
            "url": "https://docs.python.org/3/tutorial/",
            "type": "Documentation",
            "description": "Learn Python syntax, functions, classes, and modules."
        },
        {
            "name": "W3Schools Python",
            "url": "https://www.w3schools.com/python/",
            "type": "Interactive tutorial",
            "description": "Practice Python fundamentals with examples."
        }
    ],
    "sql": [
        {
            "name": "SQLBolt",
            "url": "https://sqlbolt.com/",
            "type": "Interactive practice",
            "description": "Learn SQL through lessons and exercises."
        },
        {
            "name": "W3Schools SQL",
            "url": "https://www.w3schools.com/sql/",
            "type": "Tutorial",
            "description": "Practice queries, joins, and database concepts."
        }
    ],
    "machine learning": [
        {
            "name": "Google Machine Learning Crash Course",
            "url": "https://developers.google.com/machine-learning/crash-course",
            "type": "Free course",
            "description": "Study ML concepts, models, and practical exercises."
        },
        {
            "name": "Scikit-learn User Guide",
            "url": "https://scikit-learn.org/stable/user_guide.html",
            "type": "Documentation",
            "description": "Learn how to build and evaluate ML models."
        }
    ],
    "data science": [
        {
            "name": "Kaggle Learn",
            "url": "https://www.kaggle.com/learn",
            "type": "Free micro-courses",
            "description": "Practice Python, Pandas, data visualization, and ML."
        },
        {
            "name": "Pandas Getting Started",
            "url": "https://pandas.pydata.org/docs/getting_started/",
            "type": "Documentation",
            "description": "Learn data manipulation and analysis."
        }
    ],
    "statistics": [
        {
            "name": "Khan Academy Statistics",
            "url": "https://www.khanacademy.org/math/statistics-probability",
            "type": "Free course",
            "description": "Study probability, distributions, and statistical reasoning."
        }
    ],
    "deep learning": [
        {
            "name": "PyTorch Tutorials",
            "url": "https://pytorch.org/tutorials/",
            "type": "Tutorials",
            "description": "Learn tensors, neural networks, and model training."
        },
        {
            "name": "TensorFlow Tutorials",
            "url": "https://www.tensorflow.org/tutorials",
            "type": "Tutorials",
            "description": "Practice building neural networks and deep learning models."
        }
    ],
    "nlp": [
        {
            "name": "spaCy Course",
            "url": "https://course.spacy.io/",
            "type": "Free course",
            "description": "Learn practical natural language processing."
        },
        {
            "name": "Hugging Face NLP Course",
            "url": "https://huggingface.co/learn/nlp-course",
            "type": "Free course",
            "description": "Learn transformers and modern NLP workflows."
        }
    ],
    "generative ai": [
        {
            "name": "Hugging Face Learn",
            "url": "https://huggingface.co/learn",
            "type": "Free learning",
            "description": "Explore language models, agents, and AI tools."
        }
    ],
    "java": [
        {
            "name": "Dev.java",
            "url": "https://dev.java/learn/",
            "type": "Official tutorials",
            "description": "Learn Java programming and core concepts."
        }
    ],
    "javascript": [
        {
            "name": "MDN JavaScript Guide",
            "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            "type": "Documentation",
            "description": "Learn JavaScript fundamentals and language features."
        },
        {
            "name": "javascript.info",
            "url": "https://javascript.info/",
            "type": "Tutorial",
            "description": "Study JavaScript from basics to advanced topics."
        }
    ],
    "html": [
        {
            "name": "MDN HTML",
            "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content",
            "type": "Tutorial",
            "description": "Learn how to structure web pages."
        }
    ],
    "css": [
        {
            "name": "MDN CSS",
            "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics",
            "type": "Tutorial",
            "description": "Learn styling, layout, and responsive design."
        }
    ],
    "react": [
        {
            "name": "React Learn",
            "url": "https://react.dev/learn",
            "type": "Official tutorial",
            "description": "Learn components, props, state, and React fundamentals."
        }
    ],
    "data structures": [
        {
            "name": "VisuAlgo",
            "url": "https://visualgo.net/en",
            "type": "Visual learning",
            "description": "Visualize data structures and algorithms."
        },
        {
            "name": "GeeksforGeeks",
            "url": "https://www.geeksforgeeks.org/",
            "type": "Tutorials and practice",
            "description": "Study algorithms and solve programming problems."
        }
    ],
    "git": [
        {
            "name": "Git Handbook",
            "url": "https://guides.github.com/introduction/git-handbook/",
            "type": "Guide",
            "description": "Learn version control and Git basics."
        },
        {
            "name": "Git Documentation",
            "url": "https://git-scm.com/doc",
            "type": "Documentation",
            "description": "Learn Git commands and workflows."
        }
    ],
    "docker": [
        {
            "name": "Docker Get Started",
            "url": "https://docs.docker.com/get-started/",
            "type": "Official tutorial",
            "description": "Learn container basics and build your first container."
        }
    ],
    "linux": [
        {
            "name": "Linux Journey",
            "url": "https://linuxjourney.com/",
            "type": "Free tutorial",
            "description": "Learn Linux commands and system fundamentals."
        }
    ],
    "aws": [
        {
            "name": "AWS Skill Builder",
            "url": "https://skillbuilder.aws/",
            "type": "Learning platform",
            "description": "Explore AWS training and foundational cloud concepts."
        }
    ],
    "azure": [
        {
            "name": "Microsoft Learn: Azure",
            "url": "https://learn.microsoft.com/en-us/training/azure/",
            "type": "Free learning",
            "description": "Study Azure cloud services and practical skills."
        }
    ],
    "excel": [
        {
            "name": "Microsoft Excel Help",
            "url": "https://support.microsoft.com/en-us/excel",
            "type": "Documentation",
            "description": "Learn Excel features, formulas, and analysis."
        }
    ],
    "power bi": [
        {
            "name": "Microsoft Learn: Power BI",
            "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi",
            "type": "Free learning",
            "description": "Learn data modeling, reports, and dashboards."
        }
    ]
}


def get_learning_resources(skill):
    """Return resources associated with a skill."""
    normalized = str(skill).strip().lower()

    if not normalized:
        return []

    # Exact match first.
    if normalized in RESOURCE_LIBRARY:
        return RESOURCE_LIBRARY[normalized]

    # Partial matching for related skill names.
    for key, resources in RESOURCE_LIBRARY.items():
        if key in normalized or normalized in key:
            return resources

    return [
        {
            "name": "Search free learning resources",
            "url": "https://www.google.com/search?q="
                   + normalized.replace(" ", "+")
                   + "+free+tutorial",
            "type": "Search",
            "description": "Find free tutorials and documentation for this skill."
        }
    ]


def get_resources_for_skills(skills):
    """Return a resource list for multiple skills."""
    results = []

    for skill in skills:
        resources = get_learning_resources(skill)

        results.append({
            "skill": skill,
            "resources": resources
        })

    return results