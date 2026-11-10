
LEARNING_PLANS = {
    "AI / Machine Learning": [
        {
            "topic": "Python for AI",
            "duration": "Week 1",
            "activities": [
                "Practice Python functions, loops, and data structures.",
                "Learn NumPy arrays and Pandas DataFrames.",
                "Complete a small data-cleaning exercise."
            ],
            "project": "Analyze and clean a real-world CSV dataset."
        },
        {
            "topic": "Statistics and Data Analysis",
            "duration": "Week 2",
            "activities": [
                "Review probability, mean, median, and variance.",
                "Practice correlation and data distributions.",
                "Visualize data using Matplotlib."
            ],
            "project": "Create an exploratory data analysis report."
        },
        {
            "topic": "Machine Learning",
            "duration": "Weeks 3–4",
            "activities": [
                "Study supervised and unsupervised learning.",
                "Practice regression and classification.",
                "Learn model evaluation and cross-validation."
            ],
            "project": "Build and evaluate a classification model."
        },
        {
            "topic": "Deep Learning",
            "duration": "Weeks 5–6",
            "activities": [
                "Learn neural network fundamentals.",
                "Understand activation functions and loss.",
                "Practice with a beginner deep-learning framework."
            ],
            "project": "Build a basic neural network for prediction."
        },
        {
            "topic": "AI Portfolio",
            "duration": "Week 7",
            "activities": [
                "Choose a problem and define measurable goals.",
                "Document data preparation and model choices.",
                "Write a clear README and explain results."
            ],
            "project": "Publish one complete AI project on GitHub."
        }
    ],

    "Data Science": [
        {
            "topic": "Python and Data Handling",
            "duration": "Week 1",
            "activities": [
                "Practice Python and Pandas.",
                "Handle missing values and duplicates.",
                "Practice filtering, grouping, and merging."
            ],
            "project": "Clean and analyze a public dataset."
        },
        {
            "topic": "SQL and Statistics",
            "duration": "Week 2",
            "activities": [
                "Practice SELECT, JOIN, GROUP BY, and subqueries.",
                "Review descriptive statistics.",
                "Solve practical data questions."
            ],
            "project": "Answer business questions using SQL."
        },
        {
            "topic": "Data Visualization",
            "duration": "Week 3",
            "activities": [
                "Learn Matplotlib and Seaborn.",
                "Choose suitable charts for different data.",
                "Practice explaining trends and outliers."
            ],
            "project": "Create a data storytelling report."
        },
        {
            "topic": "Machine Learning Basics",
            "duration": "Weeks 4–5",
            "activities": [
                "Learn regression and classification.",
                "Practice train-test splitting.",
                "Compare models using evaluation metrics."
            ],
            "project": "Build a predictive analytics model."
        },
        {
            "topic": "Portfolio and Communication",
            "duration": "Week 6",
            "activities": [
                "Write a project summary.",
                "Explain insights and limitations.",
                "Organize your code and documentation."
            ],
            "project": "Publish an end-to-end data science project."
        }
    ],

    "Software Development": [
        {
            "topic": "Programming Fundamentals",
            "duration": "Week 1",
            "activities": [
                "Practice functions, loops, and data structures.",
                "Review object-oriented programming.",
                "Solve beginner programming problems."
            ],
            "project": "Build a command-line application."
        },
        {
            "topic": "Data Structures and Algorithms",
            "duration": "Weeks 2–3",
            "activities": [
                "Practice arrays, strings, stacks, and queues.",
                "Learn searching and sorting.",
                "Understand time and space complexity."
            ],
            "project": "Solve and document a set of coding problems."
        },
        {
            "topic": "Backend and APIs",
            "duration": "Week 4",
            "activities": [
                "Learn HTTP and REST API fundamentals.",
                "Practice a backend framework.",
                "Learn request validation and error handling."
            ],
            "project": "Build a small REST API."
        },
        {
            "topic": "Databases and Testing",
            "duration": "Week 5",
            "activities": [
                "Practice SQL and database design.",
                "Learn unit testing.",
                "Use Git for version control."
            ],
            "project": "Connect your API to a database and test it."
        },
        {
            "topic": "Portfolio Project",
            "duration": "Week 6",
            "activities": [
                "Plan a complete application.",
                "Implement and test its core features.",
                "Document setup and usage."
            ],
            "project": "Publish a complete software project."
        }
    ],

    "Web Development": [
        {
            "topic": "HTML and CSS",
            "duration": "Week 1",
            "activities": [
                "Practice semantic HTML.",
                "Learn CSS layouts and responsive design.",
                "Build accessible page structures."
            ],
            "project": "Create a responsive personal webpage."
        },
        {
            "topic": "JavaScript",
            "duration": "Week 2",
            "activities": [
                "Practice functions, arrays, and objects.",
                "Learn DOM manipulation.",
                "Understand asynchronous JavaScript."
            ],
            "project": "Build an interactive task manager."
        },
        {
            "topic": "Frontend Framework",
            "duration": "Weeks 3–4",
            "activities": [
                "Learn components and state.",
                "Practice forms and event handling.",
                "Understand frontend routing."
            ],
            "project": "Build a multi-page frontend application."
        },
        {
            "topic": "Backend and Database",
            "duration": "Week 5",
            "activities": [
                "Learn API fundamentals.",
                "Practice server-side development.",
                "Connect an application to a database."
            ],
            "project": "Create a full-stack application."
        },
        {
            "topic": "Deployment and Portfolio",
            "duration": "Week 6",
            "activities": [
                "Practice Git and GitHub.",
                "Learn deployment fundamentals.",
                "Write project documentation."
            ],
            "project": "Deploy and document your application."
        }
    ],

    "Cloud / DevOps": [
        {
            "topic": "Linux and Networking",
            "duration": "Week 1",
            "activities": [
                "Practice Linux commands and file permissions.",
                "Learn processes and environment variables.",
                "Review DNS, HTTP, and networking basics."
            ],
            "project": "Set up and document a Linux environment."
        },
        {
            "topic": "Git and Scripting",
            "duration": "Week 2",
            "activities": [
                "Practice Git branches and merges.",
                "Write basic automation scripts.",
                "Learn shell scripting fundamentals."
            ],
            "project": "Automate a repetitive local task."
        },
        {
            "topic": "Containers",
            "duration": "Week 3",
            "activities": [
                "Learn container concepts.",
                "Practice Docker images and containers.",
                "Understand environment configuration."
            ],
            "project": "Containerize a small application."
        },
        {
            "topic": "CI/CD",
            "duration": "Week 4",
            "activities": [
                "Learn build and test pipelines.",
                "Practice automated checks.",
                "Understand deployment stages."
            ],
            "project": "Create a basic CI workflow."
        },
        {
            "topic": "Cloud Fundamentals",
            "duration": "Weeks 5–6",
            "activities": [
                "Study compute, storage, and networking services.",
                "Learn identity and access fundamentals.",
                "Review monitoring and cost awareness."
            ],
            "project": "Document a simple cloud deployment design."
        }
    ]
}


def generate_learning_plan(domain, missing_skills):
    """
    Return a domain-based plan, prioritizing topics
    related to detected missing skills.
    """

    plan = LEARNING_PLANS.get(domain, [])

    if not plan:
        return []

    missing = [
        str(skill).strip().lower()
        for skill in missing_skills
        if str(skill).strip()
    ]

    if not missing:
        return plan

    # Match missing skills to topic names and activities.
    def relevance(item):
        searchable = (
            item["topic"] + " " +
            " ".join(item["activities"]) + " " +
            item["project"]
        ).lower()

        return sum(
            1 for skill in missing
            if skill in searchable
        )

    # Preserve the original order when relevance is tied.
    indexed_plan = list(enumerate(plan))
    indexed_plan.sort(
        key=lambda pair: (-relevance(pair[1]), pair[0])
    )

    return [item for _, item in indexed_plan]