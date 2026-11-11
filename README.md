# AI Career Intelligence Agent

An AI-powered career guidance application built with Python and Streamlit. It helps users analyze resumes, identify skill gaps, explore career opportunities, and create personalized learning roadmaps.

## Features

- **Resume Analyzer:** Extracts information and skills from uploaded resumes.
- **Skill Gap Analysis:** Identifies matched and missing skills for a career domain.
- **Career Intelligence:** Builds a career profile and recommends suitable career paths.
- **Career Roadmap:** Generates a structured roadmap for career development.
- **Career Readiness:** Evaluates career readiness based on skills and profile information.
- **Job Description Matcher:** Compares a resume with a job description.
- **Personalized Learning:** Recommends learning plans and useful resources.
- **Resume Improver:** Provides suggestions to improve resume content.
- **Analysis History:** Stores and retrieves previous analysis results.

## Tech Stack

- Python
- Streamlit
- Pandas
- SQLite
- NLP and text processing
- JSON

## Project Structure

```text
AI-Career-Assistant/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── resume_parser.py
│   ├── nlp_analyzer.py
│   ├── skills_database.py
│   ├── career_profile.py
│   ├── career_domain.py
│   ├── skill_gap.py
│   ├── career_recommendations.py
│   ├── career_roadmap.py
│   ├── career_readiness.py
│   ├── job_analyzer.py
│   ├── matching_engine.py
│   ├── personalized_learning.py
│   ├── learning_resources.py
│   └── resume_improver.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/svansh246/AI-Career-Intelligence-Agent.git
```

### 2. Navigate to the project folder

```bash
cd AI-Career-Intelligence-Agent
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app/main.py
```

## Project Objective

The objective of this project is to develop an intelligent career guidance system that helps users understand their professional strengths, identify skill gaps, improve their resumes, and plan their career development.

## Author

**Vansh Sharma**

GitHub: https://github.com/svansh246

---

*Developed as an AI and Data Science project using Python and Streamlit.*
