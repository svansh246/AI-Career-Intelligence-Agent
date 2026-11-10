import re
import spacy


# ============================================================
# LOAD SPACY MODEL
# ============================================================

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None


# ============================================================
# DOMAIN SKILL DATABASE
# ============================================================

DOMAIN_SKILLS = {

    "Artificial Intelligence": [
        "python",
        "machine learning",
        "deep learning",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "natural language processing",
        "nlp",
        "computer vision",
        "statistics",
        "data structures",
        "algorithms",
        "matplotlib",
        "seaborn",
        "opencv",
        "transformers",
        "hugging face",
        "generative ai",
        "llm",
    ],

    "Machine Learning": [
        "python",
        "machine learning",
        "statistics",
        "numpy",
        "pandas",
        "scikit-learn",
        "deep learning",
        "tensorflow",
        "pytorch",
        "feature engineering",
        "model evaluation",
        "regression",
        "classification",
        "clustering",
        "data visualization",
        "matplotlib",
        "seaborn",
        "nlp",
        "computer vision",
    ],

    "Data Science": [
        "python",
        "sql",
        "statistics",
        "numpy",
        "pandas",
        "scikit-learn",
        "machine learning",
        "data analysis",
        "data visualization",
        "matplotlib",
        "seaborn",
        "power bi",
        "tableau",
        "excel",
        "deep learning",
        "nlp",
    ],

    "Data Analyst": [
        "sql",
        "excel",
        "python",
        "pandas",
        "numpy",
        "statistics",
        "data analysis",
        "data visualization",
        "power bi",
        "tableau",
        "matplotlib",
        "seaborn",
        "dashboard",
        "reporting",
    ],

    "Software Engineering": [
        "python",
        "java",
        "c++",
        "javascript",
        "data structures",
        "algorithms",
        "object oriented programming",
        "git",
        "github",
        "sql",
        "rest api",
        "api",
        "docker",
        "testing",
        "debugging",
        "software development",
    ],

    "Generative AI": [
        "python",
        "generative ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "large language models",
        "prompt engineering",
        "natural language processing",
        "nlp",
        "transformers",
        "hugging face",
        "rag",
        "retrieval augmented generation",
        "embeddings",
        "vector database",
        "langchain",
        "pytorch",
        "tensorflow",
    ],

    "Web Development": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "nodejs",
        "express",
        "rest api",
        "api",
        "git",
        "github",
        "sql",
        "mongodb",
        "typescript",
        "bootstrap",
        "frontend",
        "backend",
        "full stack",
    ],
}


# ============================================================
# SKILL PRIORITY DATABASE
# ============================================================

DOMAIN_SKILL_PRIORITY = {

    "Artificial Intelligence": {

        "high": [
            "python",
            "machine learning",
            "deep learning",
            "numpy",
            "pandas",
            "scikit-learn",
            "statistics",
            "data structures",
            "algorithms",
        ],

        "medium": [
            "tensorflow",
            "pytorch",
            "natural language processing",
            "nlp",
            "computer vision",
            "matplotlib",
            "seaborn",
            "opencv",
            "transformers",
            "hugging face",
            "generative ai",
            "llm",
        ],
    },

    "Machine Learning": {

        "high": [
            "python",
            "machine learning",
            "statistics",
            "numpy",
            "pandas",
            "scikit-learn",
            "feature engineering",
            "model evaluation",
            "regression",
            "classification",
        ],

        "medium": [
            "deep learning",
            "tensorflow",
            "pytorch",
            "clustering",
            "data visualization",
            "matplotlib",
            "seaborn",
            "nlp",
            "computer vision",
        ],
    },

    "Data Science": {

        "high": [
            "python",
            "sql",
            "statistics",
            "numpy",
            "pandas",
            "scikit-learn",
            "data analysis",
            "data visualization",
        ],

        "medium": [
            "machine learning",
            "matplotlib",
            "seaborn",
            "power bi",
            "tableau",
            "excel",
            "deep learning",
            "nlp",
        ],
    },

    "Data Analyst": {

        "high": [
            "sql",
            "excel",
            "python",
            "pandas",
            "statistics",
            "data analysis",
            "data visualization",
        ],

        "medium": [
            "numpy",
            "power bi",
            "tableau",
            "matplotlib",
            "seaborn",
            "dashboard",
            "reporting",
        ],
    },

    "Software Engineering": {

        "high": [
            "python",
            "java",
            "c++",
            "javascript",
            "data structures",
            "algorithms",
            "object oriented programming",
            "git",
            "github",
            "sql",
        ],

        "medium": [
            "rest api",
            "api",
            "docker",
            "testing",
            "debugging",
            "software development",
        ],
    },

    "Generative AI": {

        "high": [
            "python",
            "generative ai",
            "llm",
            "large language models",
            "prompt engineering",
            "natural language processing",
            "nlp",
            "transformers",
            "hugging face",
            "rag",
            "embeddings",
        ],

        "medium": [
            "machine learning",
            "deep learning",
            "retrieval augmented generation",
            "vector database",
            "langchain",
            "pytorch",
            "tensorflow",
        ],
    },

    "Web Development": {

        "high": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js",
            "nodejs",
            "rest api",
            "git",
            "github",
            "sql",
        ],

        "medium": [
            "express",
            "typescript",
            "mongodb",
            "bootstrap",
            "frontend",
            "backend",
            "full stack",
            "api",
        ],
    },
}


# ============================================================
# DOMAIN RECOMMENDATIONS
# ============================================================

DOMAIN_RECOMMENDATIONS = {

    "Artificial Intelligence": [
        "Strengthen Python and machine learning fundamentals.",
        "Build projects using deep learning frameworks such as PyTorch or TensorFlow.",
        "Practice NLP or computer vision through practical projects.",
        "Learn model evaluation and experiment tracking.",
        "Create at least one end-to-end AI project for your portfolio.",
    ],

    "Machine Learning": [
        "Strengthen Python, statistics and machine learning fundamentals.",
        "Practice regression, classification and clustering algorithms.",
        "Learn feature engineering and model evaluation.",
        "Build end-to-end machine learning projects.",
        "Document model performance using meaningful evaluation metrics.",
    ],

    "Data Science": [
        "Strengthen Python, SQL, statistics and data analysis.",
        "Practice data cleaning and exploratory data analysis.",
        "Improve data visualization using Matplotlib, Seaborn or BI tools.",
        "Build machine learning projects using real datasets.",
        "Create portfolio projects that demonstrate business insights.",
    ],

    "Data Analyst": [
        "Strengthen SQL and Excel skills.",
        "Practice data cleaning and exploratory analysis.",
        "Learn Power BI or Tableau for dashboard development.",
        "Improve statistical analysis skills.",
        "Build dashboards using real-world datasets.",
    ],

    "Software Engineering": [
        "Strengthen data structures and algorithms.",
        "Practice object-oriented programming.",
        "Improve Git and GitHub workflow knowledge.",
        "Build applications using APIs and databases.",
        "Add testing, debugging and deployment experience to projects.",
    ],

    "Generative AI": [
        "Strengthen Python and NLP fundamentals.",
        "Learn transformer architectures and large language models.",
        "Practice prompt engineering and structured prompting.",
        "Build RAG applications using embeddings and vector databases.",
        "Create practical GenAI projects using open-source models.",
    ],

    "Web Development": [
        "Strengthen HTML, CSS and JavaScript fundamentals.",
        "Build responsive frontend applications.",
        "Learn React or another modern frontend framework.",
        "Practice backend development and REST APIs.",
        "Build full-stack applications using databases.",
    ],
}


# ============================================================
# STEP 31 — LEARNING ROADMAP DATABASE
# ============================================================

LEARNING_ROADMAP = {

    "Artificial Intelligence": {

        "python": {
            "level": "Foundation",
            "action": "Strengthen Python programming fundamentals.",
            "project": "Build a Python-based data processing application.",
        },

        "numpy": {
            "level": "Foundation",
            "action": "Learn numerical computing with NumPy.",
            "project": "Create a numerical data analysis project.",
        },

        "pandas": {
            "level": "Foundation",
            "action": "Practice data manipulation and cleaning with Pandas.",
            "project": "Analyze a real-world dataset.",
        },

        "statistics": {
            "level": "Foundation",
            "action": "Learn probability, distributions and statistical concepts.",
            "project": "Perform statistical analysis on a dataset.",
        },

        "machine learning": {
            "level": "Core",
            "action": "Learn supervised and unsupervised machine learning.",
            "project": "Build a classification or regression model.",
        },

        "scikit-learn": {
            "level": "Core",
            "action": "Practice machine-learning workflows using Scikit-learn.",
            "project": "Build and evaluate multiple ML models.",
        },

        "deep learning": {
            "level": "Advanced",
            "action": "Learn neural networks and deep-learning architectures.",
            "project": "Build an image or text classification model.",
        },

        "pytorch": {
            "level": "Advanced",
            "action": "Learn PyTorch for deep-learning model development.",
            "project": "Train a neural network using PyTorch.",
        },

        "tensorflow": {
            "level": "Advanced",
            "action": "Learn TensorFlow and neural-network workflows.",
            "project": "Build and train a TensorFlow model.",
        },

        "nlp": {
            "level": "Advanced",
            "action": "Learn Natural Language Processing techniques.",
            "project": "Build a sentiment analysis or text classification system.",
        },

        "natural language processing": {
            "level": "Advanced",
            "action": "Study text preprocessing, embeddings and NLP models.",
            "project": "Build an NLP application.",
        },

        "computer vision": {
            "level": "Advanced",
            "action": "Learn image processing and computer-vision techniques.",
            "project": "Build an image classification application.",
        },

        "generative ai": {
            "level": "Advanced",
            "action": "Learn modern generative AI concepts.",
            "project": "Build a small local GenAI application.",
        },

        "llm": {
            "level": "Advanced",
            "action": "Study large language model concepts and applications.",
            "project": "Build an LLM-powered document assistant.",
        },
    },

    "Machine Learning": {

        "python": {
            "level": "Foundation",
            "action": "Strengthen Python programming for machine learning.",
            "project": "Create a Python data-analysis application.",
        },

        "statistics": {
            "level": "Foundation",
            "action": "Learn statistics and probability for ML.",
            "project": "Analyze statistical patterns in a dataset.",
        },

        "numpy": {
            "level": "Foundation",
            "action": "Learn numerical computing with NumPy.",
            "project": "Implement numerical operations on datasets.",
        },

        "pandas": {
            "level": "Foundation",
            "action": "Learn data cleaning and manipulation.",
            "project": "Perform exploratory data analysis.",
        },

        "scikit-learn": {
            "level": "Core",
            "action": "Practice machine-learning pipelines.",
            "project": "Build and compare several ML algorithms.",
        },

        "machine learning": {
            "level": "Core",
            "action": "Study supervised and unsupervised learning.",
            "project": "Build a complete ML prediction system.",
        },

        "feature engineering": {
            "level": "Core",
            "action": "Learn feature selection and transformation.",
            "project": "Improve an ML model using engineered features.",
        },

        "model evaluation": {
            "level": "Core",
            "action": "Learn accuracy, precision, recall, F1 and other metrics.",
            "project": "Compare multiple models using evaluation metrics.",
        },

        "deep learning": {
            "level": "Advanced",
            "action": "Learn neural networks and deep-learning models.",
            "project": "Build a neural-network classifier.",
        },

        "pytorch": {
            "level": "Advanced",
            "action": "Learn PyTorch model development.",
            "project": "Train a neural network with PyTorch.",
        },
    },

    "Data Science": {

        "python": {
            "level": "Foundation",
            "action": "Strengthen Python for data analysis.",
            "project": "Analyze a real-world dataset.",
        },

        "sql": {
            "level": "Foundation",
            "action": "Learn SQL queries, joins and aggregations.",
            "project": "Build a SQL-based business analysis project.",
        },

        "statistics": {
            "level": "Foundation",
            "action": "Learn descriptive and inferential statistics.",
            "project": "Perform statistical analysis on a dataset.",
        },

        "pandas": {
            "level": "Foundation",
            "action": "Master data cleaning and transformation.",
            "project": "Create an exploratory data analysis notebook.",
        },

        "numpy": {
            "level": "Foundation",
            "action": "Learn numerical data processing.",
            "project": "Perform numerical analysis using NumPy.",
        },

        "data visualization": {
            "level": "Core",
            "action": "Learn how to communicate insights visually.",
            "project": "Create an interactive data visualization project.",
        },

        "machine learning": {
            "level": "Core",
            "action": "Learn predictive modeling techniques.",
            "project": "Build a prediction model from real data.",
        },

        "power bi": {
            "level": "Core",
            "action": "Learn dashboard and business intelligence development.",
            "project": "Create a business analytics dashboard.",
        },

        "tableau": {
            "level": "Core",
            "action": "Learn Tableau visualization and dashboards.",
            "project": "Build an interactive Tableau dashboard.",
        },
    },

    "Data Analyst": {

        "sql": {
            "level": "Foundation",
            "action": "Master SQL queries and database analysis.",
            "project": "Analyze a business database using SQL.",
        },

        "excel": {
            "level": "Foundation",
            "action": "Improve Excel formulas, pivot tables and analysis.",
            "project": "Create an Excel business dashboard.",
        },

        "python": {
            "level": "Foundation",
            "action": "Learn Python for data analysis.",
            "project": "Analyze a real-world dataset.",
        },

        "pandas": {
            "level": "Foundation",
            "action": "Learn data cleaning and transformation.",
            "project": "Perform exploratory data analysis.",
        },

        "statistics": {
            "level": "Foundation",
            "action": "Strengthen statistical reasoning.",
            "project": "Analyze trends and correlations in data.",
        },

        "power bi": {
            "level": "Core",
            "action": "Learn Power BI dashboard development.",
            "project": "Build a business intelligence dashboard.",
        },

        "tableau": {
            "level": "Core",
            "action": "Learn Tableau for visual analytics.",
            "project": "Create an interactive dashboard.",
        },
    },

    "Generative AI": {

        "python": {
            "level": "Foundation",
            "action": "Strengthen Python programming.",
            "project": "Build a Python AI utility.",
        },

        "nlp": {
            "level": "Core",
            "action": "Learn Natural Language Processing.",
            "project": "Build a text classification system.",
        },

        "llm": {
            "level": "Core",
            "action": "Understand large language model concepts.",
            "project": "Build an LLM-based assistant.",
        },

        "prompt engineering": {
            "level": "Core",
            "action": "Learn structured prompt design and evaluation.",
            "project": "Create a prompt-based AI assistant.",
        },

        "transformers": {
            "level": "Advanced",
            "action": "Learn transformer architectures.",
            "project": "Experiment with a transformer-based NLP model.",
        },

        "hugging face": {
            "level": "Advanced",
            "action": "Learn Hugging Face models and datasets.",
            "project": "Deploy an open-source NLP model.",
        },

        "rag": {
            "level": "Advanced",
            "action": "Learn Retrieval-Augmented Generation.",
            "project": "Build a document-question answering system.",
        },

        "embeddings": {
            "level": "Advanced",
            "action": "Learn vector embeddings and semantic search.",
            "project": "Build a semantic document search system.",
        },

        "vector database": {
            "level": "Advanced",
            "action": "Learn vector storage and similarity search.",
            "project": "Create a local vector-search application.",
        },
    },

    "Software Engineering": {

        "python": {
            "level": "Foundation",
            "action": "Strengthen programming fundamentals.",
            "project": "Build a Python application.",
        },

        "java": {
            "level": "Foundation",
            "action": "Strengthen Java programming.",
            "project": "Build a Java application.",
        },

        "data structures": {
            "level": "Core",
            "action": "Practice arrays, trees, graphs and hash tables.",
            "project": "Implement common data structures.",
        },

        "algorithms": {
            "level": "Core",
            "action": "Practice searching, sorting and optimization.",
            "project": "Solve algorithmic programming problems.",
        },

        "git": {
            "level": "Core",
            "action": "Learn version control and Git workflows.",
            "project": "Manage a complete project using Git.",
        },

        "sql": {
            "level": "Core",
            "action": "Learn relational database concepts and SQL.",
            "project": "Build an application connected to a database.",
        },

        "rest api": {
            "level": "Advanced",
            "action": "Learn REST API design and integration.",
            "project": "Build a REST API.",
        },

        "docker": {
            "level": "Advanced",
            "action": "Learn containerization with Docker.",
            "project": "Containerize a web application.",
        },
    },

    "Web Development": {

        "html": {
            "level": "Foundation",
            "action": "Strengthen semantic HTML.",
            "project": "Build a responsive website.",
        },

        "css": {
            "level": "Foundation",
            "action": "Learn responsive layouts and modern CSS.",
            "project": "Create a responsive portfolio website.",
        },

        "javascript": {
            "level": "Core",
            "action": "Strengthen JavaScript fundamentals.",
            "project": "Build an interactive web application.",
        },

        "react": {
            "level": "Core",
            "action": "Learn component-based React development.",
            "project": "Build a React frontend.",
        },

        "node.js": {
            "level": "Core",
            "action": "Learn backend development with Node.js.",
            "project": "Build a Node.js REST API.",
        },

        "rest api": {
            "level": "Advanced",
            "action": "Learn REST API development and integration.",
            "project": "Create a full REST API.",
        },

        "sql": {
            "level": "Core",
            "action": "Learn database design and SQL.",
            "project": "Connect a web application to a database.",
        },
    },
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = str(text)

    text = text.replace(
        "\x00",
        " ",
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def normalize_text(text):
    return clean_text(
        text
    ).lower()


# ============================================================
# SKILL DETECTION
# ============================================================

def detect_skills(text):

    normalized_text = normalize_text(
        text
    )

    detected_skills = []

    all_skills = set()

    for skills in DOMAIN_SKILLS.values():

        for skill in skills:

            all_skills.add(
                skill.lower()
            )

    for skill in sorted(
        all_skills
    ):

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            normalized_text,
        ):

            detected_skills.append(
                skill
            )

    return sorted(
        list(
            set(
                detected_skills
            )
        )
    )


# ============================================================
# DOMAIN MATCHING
# ============================================================

def calculate_domain_match(
    text,
    target_domain,
    detected_skills=None,
):

    normalized_text = normalize_text(
        text
    )

    domain_skills = DOMAIN_SKILLS.get(
        target_domain,
        [],
    )

    if detected_skills is None:

        detected_skills = detect_skills(
            text
        )

    detected_lower = {
        str(skill).lower()
        for skill in detected_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in domain_skills:

        skill_lower = skill.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(skill_lower)
            + r"(?!\w)"
        )

        if (
            skill_lower in detected_lower
            or re.search(
                pattern,
                normalized_text,
            )
        ):

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    if domain_skills:

        score = (
            len(matched_skills)
            / len(domain_skills)
        ) * 100

    else:

        score = 0

    return (
        round(score, 2),
        sorted(
            list(
                set(
                    matched_skills
                )
            )
        ),
        sorted(
            list(
                set(
                    missing_skills
                )
            )
        ),
    )


# ============================================================
# SKILL GAP ENGINE
# ============================================================

def categorize_skill_gaps(
    text,
    target_domain,
    detected_skills,
):

    domain_skills = DOMAIN_SKILLS.get(
        target_domain,
        [],
    )

    priority_data = DOMAIN_SKILL_PRIORITY.get(
        target_domain,
        {},
    )

    high_priority = [
        skill.lower()
        for skill in priority_data.get(
            "high",
            [],
        )
    ]

    medium_priority = [
        skill.lower()
        for skill in priority_data.get(
            "medium",
            [],
        )
    ]

    detected_lower = {
        str(skill).lower()
        for skill in detected_skills
    }

    covered_skills = []
    high_priority_missing = []
    medium_priority_missing = []
    other_missing = []

    for skill in domain_skills:

        skill_lower = skill.lower()

        if skill_lower in detected_lower:

            covered_skills.append(
                skill
            )

        elif skill_lower in high_priority:

            high_priority_missing.append(
                skill
            )

        elif skill_lower in medium_priority:

            medium_priority_missing.append(
                skill
            )

        else:

            other_missing.append(
                skill
            )

    return {
        "covered_domain_skills": sorted(
            list(
                set(
                    covered_skills
                )
            )
        ),

        "high_priority_missing_skills": sorted(
            list(
                set(
                    high_priority_missing
                )
            )
        ),

        "medium_priority_missing_skills": sorted(
            list(
                set(
                    medium_priority_missing
                )
            )
        ),

        "other_missing_skills": sorted(
            list(
                set(
                    other_missing
                )
            )
        ),

        "skill_gap_summary": {
            "target_domain": target_domain,
            "total_domain_skills": len(
                domain_skills
            ),
            "covered": len(
                covered_skills
            ),
            "high_priority_gaps": len(
                high_priority_missing
            ),
            "medium_priority_gaps": len(
                medium_priority_missing
            ),
            "other_gaps": len(
                other_missing
            ),
        },
    }


# ============================================================
# LEARNING ROADMAP GENERATOR
# ============================================================

def generate_learning_roadmap(
    target_domain,
    high_priority_missing_skills,
    medium_priority_missing_skills,
):

    domain_roadmap = LEARNING_ROADMAP.get(
        target_domain,
        {},
    )

    roadmap = {
        "foundation": [],
        "core": [],
        "advanced": [],
        "projects": [],
    }

    all_missing_skills = (
        list(high_priority_missing_skills)
        + list(medium_priority_missing_skills)
    )

    for skill in all_missing_skills:

        skill_key = str(
            skill
        ).lower()

        data = domain_roadmap.get(
            skill_key
        )

        if not data:
            continue

        item = {
            "skill": skill,
            "level": data["level"],
            "action": data["action"],
            "project": data["project"],
        }

        level = data["level"].lower()

        if level == "foundation":

            roadmap[
                "foundation"
            ].append(item)

        elif level == "core":

            roadmap[
                "core"
            ].append(item)

        else:

            roadmap[
                "advanced"
            ].append(item)

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    for category in [
        "foundation",
        "core",
        "advanced",
    ]:

        unique_items = []
        seen = set()

        for item in roadmap[
            category
        ]:

            key = item[
                "skill"
            ].lower()

            if key not in seen:

                seen.add(
                    key
                )

                unique_items.append(
                    item
                )

        roadmap[
            category
        ] = unique_items

    # --------------------------------------------------------
    # Portfolio project roadmap
    # --------------------------------------------------------

    all_items = (
        roadmap["foundation"]
        + roadmap["core"]
        + roadmap["advanced"]
    )

    for item in all_items[:5]:

        roadmap[
            "projects"
        ].append(
            {
                "skill": item[
                    "skill"
                ],
                "project": item[
                    "project"
                ],
            }
        )

    return roadmap


# ============================================================
# EDUCATION DETECTION
# ============================================================

def detect_education(text):

    normalized_text = normalize_text(
        text
    )

    keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "b.sc",
        "bsc",
        "bca",
        "m.tech",
        "mtech",
        "master",
        "m.sc",
        "msc",
        "mca",
        "phd",
        "computer science",
        "engineering",
        "university",
        "college",
        "degree",
        "graduation",
        "education",
    ]

    detected = []

    for keyword in keywords:

        if keyword in normalized_text:

            detected.append(
                keyword
            )

    return sorted(
        list(
            set(
                detected
            )
        )
    )


# ============================================================
# EXPERIENCE DETECTION
# ============================================================

def detect_experience(text):

    normalized_text = normalize_text(
        text
    )

    keywords = [
        "experience",
        "intern",
        "internship",
        "worked",
        "work experience",
        "employment",
        "professional experience",
        "developer",
        "engineer",
        "analyst",
        "data scientist",
        "researcher",
        "trainee",
        "freelance",
    ]

    detected = []

    for keyword in keywords:

        if keyword in normalized_text:

            detected.append(
                keyword
            )

    return sorted(
        list(
            set(
                detected
            )
        )
    )


# ============================================================
# PROJECT DETECTION
# ============================================================

def detect_projects(text):

    normalized_text = normalize_text(
        text
    )

    keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "created",
        "implemented",
        "designed",
        "application",
        "system",
        "model",
        "website",
        "dashboard",
    ]

    detected = []

    for keyword in keywords:

        if keyword in normalized_text:

            detected.append(
                keyword
            )

    return sorted(
        list(
            set(
                detected
            )
        )
    )


# ============================================================
# CERTIFICATION DETECTION
# ============================================================

def detect_certifications(text):

    normalized_text = normalize_text(
        text
    )

    keywords = [
        "certification",
        "certified",
        "certificate",
        "course",
        "courses",
        "nptel",
        "coursera",
        "udemy",
        "google certificate",
        "microsoft",
        "ibm",
        "aws",
        "oracle",
    ]

    detected = []

    for keyword in keywords:

        if keyword in normalized_text:

            detected.append(
                keyword
            )

    return sorted(
        list(
            set(
                detected
            )
        )
    )


# ============================================================
# CONTACT DETECTION
# ============================================================

def detect_email(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    return bool(
        re.search(
            pattern,
            text,
        )
    )


def detect_phone(text):

    pattern = (
        r"(?<!\d)"
        r"(?:\+?\d{1,3}[\s.-]?)?"
        r"(?:\d[\s.-]?){10}"
        r"(?!\d)"
    )

    return bool(
        re.search(
            pattern,
            text,
        )
    )


def detect_github(text):

    return bool(
        re.search(
            r"github\.com",
            text,
            re.IGNORECASE,
        )
    )


def detect_linkedin(text):

    return bool(
        re.search(
            r"linkedin\.com",
            text,
            re.IGNORECASE,
        )
    )


# ============================================================
# SPACY NAMED ENTITIES
# ============================================================

def detect_named_entities(text):

    if nlp is None:
        return []

    try:

        doc = nlp(
            clean_text(text)
        )

        entities = []

        for entity in doc.ents:

            value = entity.text.strip()

            if value:

                entities.append(
                    f"{value} ({entity.label_})"
                )

        return sorted(
            list(
                set(
                    entities
                )
            )
        )

    except Exception:

        return []


# ============================================================
# ACTION WORD DETECTION
# ============================================================

def detect_action_words(text):

    normalized_text = normalize_text(
        text
    )

    action_words = [
        "developed",
        "designed",
        "implemented",
        "created",
        "built",
        "analyzed",
        "optimized",
        "improved",
        "managed",
        "led",
        "automated",
        "deployed",
        "trained",
        "evaluated",
        "integrated",
        "engineered",
        "tested",
        "maintained",
        "research",
        "researched",
    ]

    detected = []

    for word in action_words:

        if re.search(
            r"(?<!\w)"
            + re.escape(word)
            + r"(?!\w)",
            normalized_text,
        ):

            detected.append(
                word
            )

    return sorted(
        list(
            set(
                detected
            )
        )
    )


# ============================================================
# QUANTIFIED ACHIEVEMENTS
# ============================================================

def detect_quantified_achievements(text):

    patterns = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b\d+(?:\.\d+)?\s*(?:years?|months?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:users?|clients?|customers?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:projects?|models?|datasets?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:days?|weeks?|hours?)\b",
    ]

    results = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        results.extend(
            matches
        )

    return sorted(
        list(
            set(
                results
            )
        )
    )


# ============================================================
# READINESS SCORE
# ============================================================

def calculate_readiness_score(
    skills,
    domain_match_score,
    education,
    experience,
    projects,
    certifications,
    action_words,
    quantified_achievements,
):

    technical_score = min(
        len(skills) * 2.5,
        25,
    )

    domain_score = (
        domain_match_score / 100
    ) * 20

    education_score = 0

    if education:

        education_score = min(
            len(education) * 2.5,
            15,
        )

    experience_score = 0

    if experience:

        experience_score = min(
            len(experience) * 2.5,
            15,
        )

    projects_score = 0

    if projects:

        projects_score = min(
            len(projects) * 2.5,
            15,
        )

    certifications_score = 0

    if certifications:

        certifications_score = min(
            len(certifications) * 1.5,
            8,
        )

    profile_quality_score = 0

    if action_words:
        profile_quality_score += 4

    if quantified_achievements:
        profile_quality_score += 4

    profile_quality_score = min(
        profile_quality_score,
        8,
    )

    total_score = (
        technical_score
        + domain_score
        + education_score
        + experience_score
        + projects_score
        + certifications_score
        + profile_quality_score
    )

    total_score = min(
        total_score,
        100,
    )

    return {
        "total": round(
            total_score,
            2,
        ),

        "technical_skills": round(
            technical_score,
            2,
        ),

        "domain_alignment": round(
            domain_score,
            2,
        ),

        "education": round(
            education_score,
            2,
        ),

        "experience": round(
            experience_score,
            2,
        ),

        "projects": round(
            projects_score,
            2,
        ),

        "certifications": round(
            certifications_score,
            2,
        ),

        "profile_quality": round(
            profile_quality_score,
            2,
        ),
    }


# ============================================================
# STRENGTHS
# ============================================================

def generate_strengths(
    skills,
    domain_match_score,
    education,
    experience,
    projects,
    certifications,
    action_words,
    quantified_achievements,
):

    strengths = []

    if len(skills) >= 8:

        strengths.append(
            "Good technical skill coverage."
        )

    elif len(skills) >= 4:

        strengths.append(
            "The resume contains several relevant technical skills."
        )

    if domain_match_score >= 70:

        strengths.append(
            "Strong alignment with the selected career domain."
        )

    elif domain_match_score >= 40:

        strengths.append(
            "The resume shows moderate alignment with the selected career domain."
        )

    if education:

        strengths.append(
            "Education-related information was detected."
        )

    if experience:

        strengths.append(
            "Professional or internship experience was detected."
        )

    if projects:

        strengths.append(
            "Project-related experience was detected."
        )

    if certifications:

        strengths.append(
            "Certifications or professional courses were detected."
        )

    if action_words:

        strengths.append(
            "The resume uses action-oriented language."
        )

    if quantified_achievements:

        strengths.append(
            "The resume contains measurable achievements."
        )

    return strengths


# ============================================================
# WEAKNESSES
# ============================================================

def generate_weaknesses(
    skills,
    domain_match_score,
    education,
    experience,
    projects,
    certifications,
    action_words,
    quantified_achievements,
    email_detected,
    phone_detected,
    github_detected,
    linkedin_detected,
    high_priority_missing_skills,
):

    weaknesses = []

    if len(skills) < 4:

        weaknesses.append(
            "Limited technical skills were detected."
        )

    if domain_match_score < 40:

        weaknesses.append(
            "The resume has relatively low alignment with the selected career domain."
        )

    elif domain_match_score < 60:

        weaknesses.append(
            "Several skills relevant to the selected career domain are missing."
        )

    if not education:

        weaknesses.append(
            "Education information was not clearly detected."
        )

    if not experience:

        weaknesses.append(
            "Professional or internship experience was not clearly detected."
        )

    if not projects:

        weaknesses.append(
            "Project experience was not clearly detected."
        )

    if not certifications:

        weaknesses.append(
            "No certifications or courses were clearly detected."
        )

    if not action_words:

        weaknesses.append(
            "The resume could use stronger action-oriented language."
        )

    if not quantified_achievements:

        weaknesses.append(
            "Few measurable achievements were detected."
        )

    if not email_detected:

        weaknesses.append(
            "Email address was not detected."
        )

    if not phone_detected:

        weaknesses.append(
            "Phone number was not detected."
        )

    if not github_detected:

        weaknesses.append(
            "GitHub profile was not detected."
        )

    if not linkedin_detected:

        weaknesses.append(
            "LinkedIn profile was not detected."
        )

    if high_priority_missing_skills:

        top_skills = ", ".join(
            high_priority_missing_skills[:3]
        )

        weaknesses.append(
            "Important domain skills not detected: "
            f"{top_skills}."
        )

    return weaknesses


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    target_domain,
    high_priority_missing_skills,
    medium_priority_missing_skills,
    projects,
    experience,
    quantified_achievements,
):

    recommendations = []

    domain_recommendations = (
        DOMAIN_RECOMMENDATIONS.get(
            target_domain,
            [],
        )
    )

    for recommendation in domain_recommendations[:3]:

        recommendations.append(
            recommendation
        )

    if high_priority_missing_skills:

        skills_text = ", ".join(
            high_priority_missing_skills[:5]
        )

        recommendations.append(
            "Prioritize learning or demonstrating these "
            f"skills: {skills_text}."
        )

    if medium_priority_missing_skills:

        skills_text = ", ".join(
            medium_priority_missing_skills[:4]
        )

        recommendations.append(
            "After addressing the core gaps, consider "
            f"adding experience with: {skills_text}."
        )

    if not projects:

        recommendations.append(
            "Build at least two practical portfolio projects "
            f"related to {target_domain}."
        )

    if not experience:

        recommendations.append(
            "Add relevant internship, freelance, research "
            "or practical experience where possible."
        )

    if not quantified_achievements:

        recommendations.append(
            "Add measurable results to project and experience "
            "descriptions, such as accuracy, performance, "
            "time saved or dataset size."
        )

    return recommendations


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_resume(
    text,
    target_domain,
):

    text = clean_text(
        text
    )

    if not text:

        return {
            "readiness_score": 0,
            "skills": [],
            "profile": {
                "resume_length": 0,
                "skills_detected": 0,
                "domain_match_score": 0,
                "domain_matched_skills": [],
                "missing_domain_skills": [],
                "covered_domain_skills": [],
                "high_priority_missing_skills": [],
                "medium_priority_missing_skills": [],
                "other_missing_skills": [],
                "skill_gap_summary": {},
                "learning_roadmap": {},
                "education_detected": [],
                "experience_detected": [],
                "projects_detected": [],
                "certifications_detected": [],
                "email_detected": False,
                "phone_detected": False,
                "github_detected": False,
                "linkedin_detected": False,
                "named_entities": [],
                "action_words": [],
                "quantified_achievements": [],
                "score_breakdown": {},
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "target_domain": target_domain,
                "resume_text_preview": "",
            },
        }

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    skills = detect_skills(
        text
    )

    # --------------------------------------------------------
    # Domain match
    # --------------------------------------------------------

    (
        domain_match_score,
        matched_skills,
        missing_domain_skills,
    ) = calculate_domain_match(
        text,
        target_domain,
        skills,
    )

    # --------------------------------------------------------
    # Skill gaps
    # --------------------------------------------------------

    skill_gap = categorize_skill_gaps(
        text,
        target_domain,
        skills,
    )

    covered_domain_skills = skill_gap[
        "covered_domain_skills"
    ]

    high_priority_missing_skills = skill_gap[
        "high_priority_missing_skills"
    ]

    medium_priority_missing_skills = skill_gap[
        "medium_priority_missing_skills"
    ]

    other_missing_skills = skill_gap[
        "other_missing_skills"
    ]

    skill_gap_summary = skill_gap[
        "skill_gap_summary"
    ]

    # --------------------------------------------------------
    # Learning roadmap
    # --------------------------------------------------------

    learning_roadmap = generate_learning_roadmap(
        target_domain=target_domain,
        high_priority_missing_skills=(
            high_priority_missing_skills
        ),
        medium_priority_missing_skills=(
            medium_priority_missing_skills
        ),
    )

    # --------------------------------------------------------
    # Resume sections
    # --------------------------------------------------------

    education = detect_education(
        text
    )

    experience = detect_experience(
        text
    )

    projects = detect_projects(
        text
    )

    certifications = detect_certifications(
        text
    )

    # --------------------------------------------------------
    # Contact
    # --------------------------------------------------------

    email_detected = detect_email(
        text
    )

    phone_detected = detect_phone(
        text
    )

    github_detected = detect_github(
        text
    )

    linkedin_detected = detect_linkedin(
        text
    )

    # --------------------------------------------------------
    # NLP
    # --------------------------------------------------------

    named_entities = detect_named_entities(
        text
    )

    action_words = detect_action_words(
        text
    )

    quantified_achievements = (
        detect_quantified_achievements(
            text
        )
    )

    # --------------------------------------------------------
    # Score
    # --------------------------------------------------------

    score_data = calculate_readiness_score(
        skills=skills,
        domain_match_score=domain_match_score,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
        action_words=action_words,
        quantified_achievements=quantified_achievements,
    )

    readiness_score = score_data[
        "total"
    ]

    # --------------------------------------------------------
    # Strengths
    # --------------------------------------------------------

    strengths = generate_strengths(
        skills=skills,
        domain_match_score=domain_match_score,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
        action_words=action_words,
        quantified_achievements=quantified_achievements,
    )

    # --------------------------------------------------------
    # Weaknesses
    # --------------------------------------------------------

    weaknesses = generate_weaknesses(
        skills=skills,
        domain_match_score=domain_match_score,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
        action_words=action_words,
        quantified_achievements=quantified_achievements,
        email_detected=email_detected,
        phone_detected=phone_detected,
        github_detected=github_detected,
        linkedin_detected=linkedin_detected,
        high_priority_missing_skills=(
            high_priority_missing_skills
        ),
    )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        target_domain=target_domain,
        high_priority_missing_skills=(
            high_priority_missing_skills
        ),
        medium_priority_missing_skills=(
            medium_priority_missing_skills
        ),
        projects=projects,
        experience=experience,
        quantified_achievements=(
            quantified_achievements
        ),
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {

        "readiness_score": readiness_score,

        "skills": skills,

        "profile": {

            "resume_length": len(
                text
            ),

            "skills_detected": len(
                skills
            ),

            "domain_match_score": (
                domain_match_score
            ),

            "domain_matched_skills": (
                matched_skills
            ),

            "missing_domain_skills": (
                missing_domain_skills
            ),

            "covered_domain_skills": (
                covered_domain_skills
            ),

            "high_priority_missing_skills": (
                high_priority_missing_skills
            ),

            "medium_priority_missing_skills": (
                medium_priority_missing_skills
            ),

            "other_missing_skills": (
                other_missing_skills
            ),

            "skill_gap_summary": (
                skill_gap_summary
            ),

            "learning_roadmap": (
                learning_roadmap
            ),

            "education_detected": education,

            "experience_detected": experience,

            "projects_detected": projects,

            "certifications_detected": certifications,

            "email_detected": email_detected,

            "phone_detected": phone_detected,

            "github_detected": github_detected,

            "linkedin_detected": linkedin_detected,

            "named_entities": named_entities,

            "action_words": action_words,

            "quantified_achievements": (
                quantified_achievements
            ),

            "score_breakdown": {

                "technical_skills": (
                    score_data[
                        "technical_skills"
                    ]
                ),

                "domain_alignment": (
                    score_data[
                        "domain_alignment"
                    ]
                ),

                "education": (
                    score_data[
                        "education"
                    ]
                ),

                "experience": (
                    score_data[
                        "experience"
                    ]
                ),

                "projects": (
                    score_data[
                        "projects"
                    ]
                ),

                "certifications": (
                    score_data[
                        "certifications"
                    ]
                ),

                "profile_quality": (
                    score_data[
                        "profile_quality"
                    ]
                ),
            },

            "strengths": strengths,

            "weaknesses": weaknesses,

            "recommendations": recommendations,

            "target_domain": target_domain,

            "resume_text_preview": text[
                :2500
            ],
        },
    }