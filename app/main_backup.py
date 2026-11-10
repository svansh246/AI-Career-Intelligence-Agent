
import io
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None


# ============================================================
# CONFIGURATION
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DB_PATH = PROJECT_DIR / "career_assistant.db"

st.set_page_config(
    page_title="AI Career Intelligence Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.hero {
    padding: 1.5rem;
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 18px;
    margin-bottom: 1rem;
}
.small-muted {
    opacity: .75;
    font-size: .9rem;
}
div[data-testid="stMetric"] {
    padding: 1rem;
    border: 1px solid rgba(128,128,128,.22);
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                filename TEXT,
                skills TEXT,
                education TEXT,
                experience TEXT,
                certificates TEXT,
                projects TEXT,
                recommended_role TEXT,
                match_score INTEGER,
                full_analysis TEXT
            )
        """)

        existing = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(analysis_history)"
            ).fetchall()
        }

        required = {
            "created_at": "TEXT",
            "filename": "TEXT",
            "skills": "TEXT",
            "education": "TEXT",
            "experience": "TEXT",
            "certificates": "TEXT",
            "projects": "TEXT",
            "recommended_role": "TEXT",
            "match_score": "INTEGER",
            "full_analysis": "TEXT",
        }

        for column, datatype in required.items():
            if column not in existing:
                conn.execute(
                    f"ALTER TABLE analysis_history "
                    f"ADD COLUMN {column} {datatype}"
                )


def save_analysis(filename, parsed, skills, role, score):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO analysis_history (
                created_at, filename, skills, education, experience,
                certificates, projects, recommended_role, match_score,
                full_analysis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename,
            json.dumps(skills, ensure_ascii=False),
            json.dumps(parsed["education"], ensure_ascii=False),
            json.dumps(parsed["experience"], ensure_ascii=False),
            json.dumps(parsed["certificates"], ensure_ascii=False),
            json.dumps(parsed["projects"], ensure_ascii=False),
            role,
            score,
            json.dumps(parsed["sections"], ensure_ascii=False),
        ))


def get_history():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM analysis_history ORDER BY id DESC"
        ).fetchall()


def safe_json_list(value):
    try:
        result = json.loads(value or "[]")
        return result if isinstance(result, list) else []
    except (ValueError, TypeError):
        return []


init_database()


# ============================================================
# TEXT NORMALIZATION AND EXTRACTION
# ============================================================

def normalize_resume_text(text):
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = text.replace("\uf0b7", "•")
    text = text.replace("\u2022", "•")
    text = text.replace("\u25aa", "•")
    text = text.replace("\u25cf", "•")

    # Remove common Markdown formatting.
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")

    # Standardize bullet characters.
    text = re.sub(r"(?m)^\s*[•●▪◦]\s*", "- ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT."""
    if uploaded_file is None:
        return "", "Please upload a resume."

    filename = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    try:
        if filename.endswith(".pdf"):
            if PdfReader is None:
                return "", (
                    "PDF support is missing. Run:\n"
                    "python -m pip install pypdf"
                )

            reader = PdfReader(io.BytesIO(data))

            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except Exception:
                    return "", (
                        "This PDF is password-protected. "
                        "Upload an unlocked PDF."
                    )

            pages = []

            for page in reader.pages:
                try:
                    pages.append(page.extract_text() or "")
                except Exception:
                    pages.append("")

            text = "\n".join(pages)

        elif filename.endswith(".docx"):
            if Document is None:
                return "", (
                    "DOCX support is missing. Run:\n"
                    "python -m pip install python-docx"
                )

            document = Document(io.BytesIO(data))

            lines = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            # Include text inside tables.
            for table in document.tables:
                for row in table.rows:
                    cells = [
                        cell.text.strip()
                        for cell in row.cells
                    ]

                    if any(cells):
                        lines.append(" | ".join(cells))

            text = "\n".join(lines)

        elif filename.endswith(".txt"):
            text = data.decode("utf-8", errors="replace")

        else:
            return "", (
                "Unsupported file type. Upload PDF, DOCX, or TXT."
            )

        text = normalize_resume_text(text)

        if not text:
            return "", (
                "No readable text was extracted. If this is a scanned "
                "PDF, OCR is required. Try a searchable PDF or DOCX."
            )

        return text, ""

    except Exception as exc:
        return "", f"Could not read the file: {exc}"


# ============================================================
# SECTION DETECTION
# ============================================================

SECTION_ALIASES = {
    "Contact": [
        "contact information",
        "contact details",
        "personal details",
    ],
    "Summary": [
        "professional summary",
        "profile summary",
        "career objective",
        "professional profile",
        "about me",
        "summary",
        "objective",
    ],
    "Skills": [
        "technical skills",
        "key skills",
        "core competencies",
        "skills listed in resume",
        "skills",
    ],
    "Education": [
        "educational qualifications",
        "academic qualifications",
        "academic background",
        "education",
    ],
    "Experience": [
        "professional experience",
        "work experience",
        "internship experience",
        "employment history",
        "professional background",
        "internships",
        "experience",
    ],
    "Certificates / Achievements": [
        "certifications and achievements",
        "certificates and achievements",
        "achievements and awards",
        "certifications and awards",
        "certification courses",
        "certification and training",
        "courses and certifications",
        "certifications",
        "certificates",
        "achievements",
        "awards",
        "courses",
    ],
    "Projects": [
        "academic projects",
        "technical projects",
        "personal projects",
        "project experience",
        "key projects",
        "projects",
    ],
}

ALL_ALIASES = sorted(
    [
        (alias, section)
        for section, aliases in SECTION_ALIASES.items()
        for alias in aliases
    ],
    key=lambda item: len(item[0]),
    reverse=True,
)


def normalize_heading(line):
    line = line.strip().lower()
    line = re.sub(r"^\s*#{1,6}\s*", "", line)
    line = line.replace("**", "").strip()
    line = re.sub(r"[\s:|–—-]+$", "", line)
    return re.sub(r"\s+", " ", line).strip()


def recognize_heading(line):
    """
    Detect section headings at the start of a line.
    Supports plain headings and headings followed by content.
    """
    cleaned = line.strip()
    cleaned = re.sub(r"^\s*#{1,6}\s*", "", cleaned)
    cleaned = cleaned.replace("**", "").strip()
    normalized = normalize_heading(cleaned)

    for alias, section in ALL_ALIASES:
        if normalized == alias:
            return section, ""

        pattern = (
            r"(?i)^" + re.escape(alias)
            + r"\s*[:|–—-]\s*(.*)$"
        )

        match = re.match(pattern, cleaned)

        if match:
            return section, match.group(1).strip()

    return None, ""


def extract_all_sections(text):
    """
    Divide the extracted resume into sections.
    Original extracted text is retained separately for troubleshooting.
    """
    text = normalize_resume_text(text)

    sections = {}
    current = None
    buffer = []

    def save_current():
        if current:
            content = "\n".join(buffer).strip()

            if content:
                if current in sections:
                    sections[current] += "\n" + content
                else:
                    sections[current] = content

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            if current:
                buffer.append("")
            continue

        section, remainder = recognize_heading(line)

        if section:
            save_current()
            current = section
            buffer = []

            if remainder:
                buffer.append(remainder)

            continue

        if current:
            buffer.append(line)

    save_current()

    return sections


# ============================================================
# ENTRY PARSING
# ============================================================

def clean_line(line):
    line = line.strip()

    # Remove a leading bullet or number only.
    line = re.sub(r"^\s*[-•●▪◦*]\s*", "", line)
    line = re.sub(r"^\s*\d{1,3}\s*[.)]\s*", "", line)
    line = re.sub(r"\s+", " ", line)

    return line.strip(" \t|")


def split_known_entries(text):
    """
    Keep separate source lines as entries.
    Do not split a sentence into multiple entries just because it contains
    punctuation or numbers.
    """
    if not text:
        return []

    entries = []

    for raw_line in normalize_resume_text(text).splitlines():
        line = clean_line(raw_line)

        if not line:
            continue

        if line.lower() in {
            "none",
            "nil",
            "n/a",
            "not applicable",
        }:
            continue

        if re.fullmatch(r"[\W_]+", line):
            continue

        entries.append(line)

    unique = []
    seen = set()

    for entry in entries:
        key = entry.casefold()

        if key not in seen:
            unique.append(entry)
            seen.add(key)

    return unique


def split_education_entries(text):
    return split_known_entries(text)


def split_experience_entries(text):
    return split_known_entries(text)


def split_certificate_entries(text):
    """
    Preserve certification titles, course providers, and achievement
    descriptions, whether or not a date is present.
    """
    return split_known_entries(text)


PROJECT_DESCRIPTION_STARTS = (
    "demonstrates ",
    "responsible for ",
    "developed ",
    "created ",
    "implemented ",
    "built ",
    "designed ",
    "worked on ",
    "used ",
    "the project ",
    "this project ",
    "committed to ",
    "contributed to ",
    "leveraged ",
    "technologies used",
    "tools used",
    "key features",
    "features:",
    "description:",
    "objective:",
    "internships",
    "demonstrates excellent",
)


def is_project_title(line):
    """
    Estimate whether a line is a project title rather than a description.
    """
    value = clean_line(line)

    if not value or len(value) > 110:
        return False

    lower = value.lower()

    if lower.startswith(PROJECT_DESCRIPTION_STARTS):
        return False

    if re.search(r"[.!?]$", value):
        return False

    # A colon often indicates a title followed by a subtitle.
    if ":" in value:
        return True

    # Common words found in project titles.
    if re.search(
        r"(?i)\b(project|system|application|assistant|dashboard|"
        r"prediction|detection|analysis|platform|game|website|"
        r"model|tool|portal|classifier)\b",
        value,
    ):
        return True

    # Allow short standalone titles.
    words = value.split()

    if len(words) <= 7 and value.istitle():
        return True

    return False


def split_project_entries(text):
    """
    Group each project's description lines into a single project entry.
    Numbered descriptions do not automatically become new projects.
    """
    if not text:
        return []

    lines = [
        line.strip()
        for line in normalize_resume_text(text).splitlines()
        if line.strip()
    ]

    lines = [
        line for line in lines
        if normalize_heading(line) not in {
            "projects",
            "academic projects",
            "personal projects",
            "technical projects",
            "key projects",
        }
    ]

    if not lines:
        return []

    projects = []
    current = []

    def save_project():
        if not current:
            return

        title = clean_line(current[0])
        details = [clean_line(item) for item in current[1:]]
        details = [item for item in details if item]

        result = title

        if details:
            result += "\n" + "\n".join(
                f"• {item}" for item in details
            )

        projects.append(result)

    for line in lines:
        if current and is_project_title(line):
            save_project()
            current = [line]
        elif not current:
            current = [line]
        else:
            current.append(line)

    save_project()

    return projects


def parse_resume_sections(resume_text):
    sections = extract_all_sections(resume_text)

    return {
        "sections": sections,
        "education": split_education_entries(
            sections.get("Education", "")
        ),
        "experience": split_experience_entries(
            sections.get("Experience", "")
        ),
        "certificates": split_certificate_entries(
            sections.get("Certificates / Achievements", "")
        ),
        "projects": split_project_entries(
            sections.get("Projects", "")
        ),
    }


# ============================================================
# SKILL DETECTION
# ============================================================

SKILL_DICTIONARY = {
    "Python": ["python"],
    "Java": ["java"],
    "C": ["c programming"],
    "C++": ["c++"],
    "JavaScript": ["javascript", "java script"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql"],
    "Data Science": ["data science"],
    "Data Analysis": ["data analysis", "data analyst"],
    "Machine Learning": ["machine learning", "ml models"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": [
        "artificial intelligence",
        "ai/ml",
    ],
    "Generative AI": ["generative ai", "genai", "gen ai"],
    "LLMs": ["llm", "large language model"],
    "RAG": ["retrieval augmented generation"],
    "NLP": ["natural language processing", "nlp"],
    "Computer Vision": ["computer vision", "opencv"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Excel": ["excel", "spreadsheets"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Statistics": ["statistics", "statistical analysis"],
    "Data Visualization": [
        "data visualization",
        "data visualisation",
    ],
    "Git": ["github", "git"],
    "Docker": ["docker"],
    "AWS": ["amazon web services", "aws"],
    "Azure": ["microsoft azure", "azure"],
    "HTML": ["html5", "html"],
    "CSS": ["css3", "css"],
    "Node.js": ["node.js", "nodejs"],
    "Streamlit": ["streamlit"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Communication": [
        "effective communication",
        "communication skills",
    ],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Critical Thinking": ["critical thinking"],
    "Teamwork": ["teamwork", "team work"],
}


def detect_skills(text):
    text_lower = text.lower()
    found = []

    for skill, keywords in SKILL_DICTIONARY.items():
        for keyword in keywords:
            if keyword in {"c", "java", "git", "sql"}:
                pattern = (
                    r"(?<![a-z])"
                    + re.escape(keyword)
                    + r"(?![a-z])"
                )

                if re.search(pattern, text_lower):
                    found.append(skill)
                    break

            elif keyword in text_lower:
                found.append(skill)
                break

    return sorted(set(found))


# ============================================================
# CAREER MATCHING AND ROADMAPS
# ============================================================

JOB_ROLES = {
    "Data Analyst": {
        "skills": [
            "Python", "SQL", "MySQL", "Excel", "Power BI",
            "Tableau", "Statistics", "Data Analysis",
            "Data Visualization", "Pandas",
        ],
        "roadmap": [
            "Strengthen SQL joins, aggregations and window functions.",
            "Practice Excel dashboards and data cleaning.",
            "Learn Power BI or Tableau.",
            "Practice statistics, exploratory analysis and KPIs.",
            "Publish two portfolio projects with business insights.",
        ],
    },
    "Data Scientist": {
        "skills": [
            "Python", "SQL", "Statistics", "Data Science",
            "Machine Learning", "Pandas", "NumPy",
            "Scikit-learn", "Data Visualization",
        ],
        "roadmap": [
            "Revise Python, Pandas, NumPy and exploratory analysis.",
            "Build probability and statistics fundamentals.",
            "Train regression, classification and clustering models.",
            "Evaluate models using suitable metrics and validation.",
            "Deploy and document an end-to-end project.",
        ],
    },
    "Machine Learning Engineer": {
        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "Scikit-learn", "TensorFlow", "PyTorch",
            "Git", "Docker", "SQL",
        ],
        "roadmap": [
            "Master Python and model evaluation.",
            "Build supervised and unsupervised ML projects.",
            "Learn one deep learning framework.",
            "Learn APIs, testing, Docker and deployment.",
            "Build a reproducible ML pipeline.",
        ],
    },
    "AI / Generative AI Engineer": {
        "skills": [
            "Python", "Artificial Intelligence", "Generative AI",
            "LLMs", "RAG", "NLP", "SQL", "Git",
        ],
        "roadmap": [
            "Strengthen Python, APIs and JSON.",
            "Learn embeddings, transformers and LLM evaluation.",
            "Build a document question-answering app using RAG.",
            "Add source citations, tests and safeguards.",
            "Deploy an AI application and document its limitations.",
        ],
    },
    "Data Engineer": {
        "skills": [
            "Python", "SQL", "MySQL", "PostgreSQL",
            "Git", "Docker", "AWS", "Azure",
        ],
        "roadmap": [
            "Improve SQL and database modelling.",
            "Write Python extraction and transformation pipelines.",
            "Learn ETL/ELT and data quality checks.",
            "Explore cloud platforms and orchestration.",
            "Build a scheduled pipeline with logging.",
        ],
    },
    "Python Developer": {
        "skills": [
            "Python", "SQL", "Git", "Flask", "Django",
            "HTML", "CSS", "JavaScript", "Docker",
        ],
        "roadmap": [
            "Strengthen Python, functions, OOP and exception handling.",
            "Practice unit testing, Git and project structure.",
            "Build a REST API using Flask or Django.",
            "Connect a database and implement validation.",
            "Deploy and document a tested application.",
        ],
    },
}


def calculate_role_matches(skills):
    skill_set = {skill.casefold() for skill in skills}
    results = []

    for role, details in JOB_ROLES.items():
        required = details["skills"]

        matched = [
            skill for skill in required
            if skill.casefold() in skill_set
        ]

        missing = [
            skill for skill in required
            if skill.casefold() not in skill_set
        ]

        score = round(100 * len(matched) / len(required))

        results.append({
            "role": role,
            "score": score,
            "matched": matched,
            "missing": missing,
            "roadmap": details["roadmap"],
        })

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )


# ============================================================
# DISPLAY HELPERS
# ============================================================

def show_entries(title, entries):
    st.subheader(title)

    if not entries:
        st.info(
            "No structured entries detected. Open Diagnostics to inspect "
            "the extracted text and recognized section headings."
        )
        return

    for index, entry in enumerate(entries, start=1):
        lines = entry.splitlines()
        first_line = lines[0] if lines else entry

        with st.container(border=True):
            st.markdown(f"**{index}. {first_line}**")

            for line in lines[1:]:
                item = line.strip()

                if item:
                    st.markdown(f"- {item.lstrip('•- ')}")


def display_section_debug(sections):
    if not sections:
        st.warning("No section headings were recognized.")
        return

    for name, content in sections.items():
        with st.expander(
            f"{name} — {len(content)} characters"
        ):
            st.text(content or "(Empty section)")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("🚀 Career Intelligence")
    st.caption("AI-powered resume analysis")

    page = st.radio(
        "Navigation",
        [
            "Resume Analyzer",
            "Career Roadmap",
            "Analysis History",
            "About Project",
        ],
    )

    st.divider()
    st.caption("Local database: career_assistant.db")
    st.caption("Formats: PDF, DOCX, TXT")


# ============================================================
# RESUME ANALYZER
# ============================================================

if page == "Resume Analyzer":
    st.markdown("""
    <div class="hero">
        <h1>AI Career Intelligence Assistant</h1>
        <p>Understand your resume and discover your next career steps.</p>
        <p class="small-muted">
        Extract skills, education, internships, certificates and projects
        from one uploaded file.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        help="A searchable PDF or DOCX usually gives the best results.",
    )

    analyze_clicked = st.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None),
    )

    if analyze_clicked and uploaded_file is not None:
        with st.spinner("Extracting and organizing your resume..."):
            resume_text, error = extract_text(uploaded_file)

            if error:
                st.error(error)
                st.stop()

            parsed = parse_resume_sections(resume_text)
            skills = detect_skills(resume_text)
            matches = calculate_role_matches(skills)

            best_role = matches[0]["role"] if matches else "Not determined"
            best_score = matches[0]["score"] if matches else 0

            try:
                save_analysis(
                    uploaded_file.name,
                    parsed,
                    skills,
                    best_role,
                    best_score,
                )
            except sqlite3.Error as exc:
                st.warning(
                    f"Analysis completed, but history could not be saved: {exc}"
                )

            st.session_state["resume_text"] = resume_text
            st.session_state["parsed_resume"] = parsed
            st.session_state["detected_skills"] = skills
            st.session_state["role_matches"] = matches
            st.session_state["analyzed_filename"] = uploaded_file.name

        st.success("Resume analysis completed.")

    if "parsed_resume" not in st.session_state:
        st.info("Upload your resume and click Analyze Resume to begin.")

    else:
        parsed = st.session_state["parsed_resume"]
        skills = st.session_state["detected_skills"]
        matches = st.session_state["role_matches"]

        st.caption(
            f"Analyzed file: {st.session_state['analyzed_filename']}"
        )

        st.subheader("Analysis Overview")

        a, b, c, d, e = st.columns(5)
        a.metric("Skills", len(skills))
        b.metric("Education", len(parsed["education"]))
        c.metric("Experience", len(parsed["experience"]))
        d.metric("Projects", len(parsed["projects"]))
        e.metric("Certificates", len(parsed["certificates"]))

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Skills",
            "Education",
            "Experience",
            "Projects",
            "Certificates",
        ])

        with tab1:
            st.subheader("Detected Skills")

            if skills:
                st.markdown(" · ".join(f"`{skill}`" for skill in skills))
            else:
                st.info(
                    "No known skills matched the current skill dictionary."
                )

            original = parsed["sections"].get("Skills", "")

            if original:
                with st.expander("Original skills section"):
                    st.text(original)

        with tab2:
            show_entries(
                "Education and Qualifications",
                parsed["education"],
            )

        with tab3:
            show_entries(
                "Experience and Internships",
                parsed["experience"],
            )

        with tab4:
            show_entries("Projects", parsed["projects"])

        with tab5:
            show_entries(
                "Certificates and Achievements",
                parsed["certificates"],
            )

        st.divider()
        st.subheader("Recommended Career Roles")
        st.caption(
            "Scores represent overlap with predefined role skills. "
            "They are not hiring probabilities."
        )

        for index, item in enumerate(matches):
            with st.expander(
                f"{item['role']} — {item['score']}% skill overlap",
                expanded=(index == 0),
            ):
                st.progress(item["score"] / 100)

                left, right = st.columns(2)

                with left:
                    st.markdown("**Skills matched**")
                    st.write(", ".join(item["matched"]) or "No matches yet.")

                with right:
                    st.markdown("**Skills to develop**")
                    st.write(
                        ", ".join(item["missing"])
                        or "All listed skills matched."
                    )

                st.markdown("**Suggested roadmap**")

                for number, step in enumerate(
                    item["roadmap"], start=1
                ):
                    st.markdown(f"{number}. {step}")

        st.divider()
        st.subheader("Diagnostics")

        with st.expander("Debug: extracted resume text"):
            st.caption(
                "This is the text extracted from the uploaded file."
            )
            st.text(st.session_state["resume_text"])

        with st.expander("Debug: detected section boundaries"):
            display_section_debug(parsed.get("sections", {}))

        with st.expander("Debug: complete structured result"):
            st.json({
                "skills": skills,
                "education": parsed["education"],
                "experience": parsed["experience"],
                "certificates": parsed["certificates"],
                "projects": parsed["projects"],
            })

        export_data = {
            "filename": st.session_state["analyzed_filename"],
            "analysis_date": datetime.now().isoformat(timespec="seconds"),
            "skills": skills,
            "sections": parsed["sections"],
            "education": parsed["education"],
            "experience": parsed["experience"],
            "certificates": parsed["certificates"],
            "projects": parsed["projects"],
            "role_matches": matches,
        }

        st.download_button(
            "Download Complete Analysis (JSON)",
            data=json.dumps(
                export_data,
                indent=2,
                ensure_ascii=False,
            ),
            file_name="career_analysis.json",
            mime="application/json",
            use_container_width=True,
        )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif page == "Career Roadmap":
    st.title("Career Roadmap")
    st.write("Choose a target career to view its learning plan.")

    selected_role = st.selectbox(
        "Target role",
        list(JOB_ROLES.keys()),
    )

    st.subheader(selected_role)

    for number, step in enumerate(
        JOB_ROLES[selected_role]["roadmap"],
        start=1,
    ):
        with st.container(border=True):
            st.markdown(f"**Step {number}**")
            st.write(step)

    st.caption(
        "This is a rule-based learning plan. Adapt it to your goals."
    )


# ============================================================
# ANALYSIS HISTORY
# ============================================================

elif page == "Analysis History":
    st.title("Analysis History")
    st.write("Previously analyzed resumes saved in SQLite.")

    try:
        history = get_history()
    except sqlite3.Error as exc:
        st.error(f"Could not load history: {exc}")
        history = []

    if not history:
        st.info("No saved analyses yet. Analyze a resume first.")

    else:
        st.caption(f"Saved analyses: {len(history)}")

        for row in history:
            filename = row["filename"] or "Unnamed resume"
            timestamp = row["created_at"] or "Unknown date"

            with st.expander(f"{filename} — {timestamp}"):
                left, right = st.columns(2)

                left.metric(
                    "Recommended role",
                    row["recommended_role"] or "Not determined",
                )
                right.metric(
                    "Skill overlap",
                    f"{row['match_score'] or 0}%",
                )

                st.markdown("**Skills**")
                st.write(
                    ", ".join(safe_json_list(row["skills"])) or "None"
                )

                show_entries(
                    "Education",
                    safe_json_list(row["education"]),
                )
                show_entries(
                    "Experience",
                    safe_json_list(row["experience"]),
                )
                show_entries(
                    "Projects",
                    safe_json_list(row["projects"]),
                )
                show_entries(
                    "Certificates / Achievements",
                    safe_json_list(row["certificates"]),
                )

                record = {
                    "filename": filename,
                    "created_at": timestamp,
                    "skills": safe_json_list(row["skills"]),
                    "education": safe_json_list(row["education"]),
                    "experience": safe_json_list(row["experience"]),
                    "projects": safe_json_list(row["projects"]),
                    "certificates": safe_json_list(row["certificates"]),
                    "recommended_role": row["recommended_role"],
                    "match_score": row["match_score"],
                }

                st.download_button(
                    "Download this analysis",
                    data=json.dumps(
                        record,
                        indent=2,
                        ensure_ascii=False,
                    ),
                    file_name=f"analysis_{row['id']}.json",
                    mime="application/json",
                    key=f"history_download_{row['id']}",
                )


# ============================================================
# ABOUT
# ============================================================

elif page == "About Project":
    st.title("About This Project")

    st.markdown("""
    ## AI Career Intelligence Assistant

    A Python and Streamlit application for resume analysis and career planning.

    **Features**
    - PDF, DOCX and TXT text extraction
    - Resume section detection
    - Skills identification
    - Education and internship extraction
    - Grouped project descriptions
    - Certificate and achievement extraction
    - Rule-based career-role matching
    - Learning roadmaps
    - Local SQLite history
    - JSON export and diagnostic panels

    **Technology stack**
    - Python
    - Streamlit
    - pypdf
    - python-docx
    - SQLite
    - Regular expressions

    **Limitations:** scanned PDFs may need OCR. Unusual layouts and
    merged headings may require specific parsing rules. Career-match
    scores are based on predefined skills, not hiring probabilities.
    """)
