import re


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(text):
    """Clean unnecessary spaces and bullet characters."""

    text = text.replace("\r", " ")
    text = text.replace("\t", " ")

    text = re.sub(r"\s+", " ", text)

    text = text.strip(" •❖:-")

    return text.strip()


def unique_list(items):
    """Remove duplicates while preserving order."""

    result = []
    seen = set()

    for item in items:

        item = clean_text(item)

        if not item:
            continue

        key = item.lower()

        if key not in seen:

            seen.add(key)
            result.append(item)

    return result


# ============================================================
# SECTION DETECTION
# ============================================================

SECTION_NAMES = {
    "education": [
        "education"
    ],

    "experience": [
        "internship/work experience",
        "internship",
        "work experience",
        "experience"
    ],

    "certifications": [
        "participation / achievement",
        "participation/achievement",
        "achievements",
        "certifications",
        "certification"
    ],

    "skills": [
        "skills and tools",
        "skills & tools",
        "technical skills",
        "skills"
    ],

    "soft_skills": [
        "soft skills"
    ],

    "projects": [
        "projects",
        "project"
    ]
}


def detect_section(line):

    line_lower = line.lower().strip()

    for section, names in SECTION_NAMES.items():

        for name in names:

            if name in line_lower:

                return section

    return None


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_sections(text):

    lines = text.splitlines()

    sections = {
        "profile": [],
        "education": [],
        "experience": [],
        "certifications": [],
        "skills": [],
        "soft_skills": [],
        "projects": []
    }

    current_section = "profile"

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        detected_section = detect_section(
            clean_line
        )

        if detected_section:

            current_section = detected_section

            continue

        sections[current_section].append(
            clean_line
        )

    return sections


# ============================================================
# PROFILE EXTRACTION
# ============================================================

def extract_profile(sections):

    profile_lines = sections.get(
        "profile",
        []
    )

    profile_text = " ".join(
        profile_lines
    )

    return clean_text(profile_text)


# ============================================================
# EDUCATION EXTRACTION
# ============================================================

def extract_education(sections):

    lines = sections.get(
        "education",
        []
    )

    education = []

    current_entry = None

    for line in lines:

        clean_line = clean_text(line)

        if not clean_line:
            continue

        # Ignore table heading
        if (
            "degree" in clean_line.lower()
            and "institution" in clean_line.lower()
        ):
            continue

        # Detect degree
        if (
            "b.tech" in clean_line.lower()
            or "btech" in clean_line.lower()
            or "b.e" in clean_line.lower()
            or "bachelor" in clean_line.lower()
            or "m.tech" in clean_line.lower()
            or "mtech" in clean_line.lower()
            or "master" in clean_line.lower()
            or "class 12" in clean_line.lower()
        ):

            current_entry = {
                "degree": clean_line,
                "institution": "",
                "year": "",
                "score": ""
            }

            education.append(
                current_entry
            )

            continue

        # Add information to current entry
        if current_entry:

            # Year / duration
            year_match = re.search(
                r"\b20\d{2}\s*[–-]\s*20\d{2}\b",
                clean_line
            )

            single_year_match = re.search(
                r"\b20\d{2}\b",
                clean_line
            )

            cgpa_match = re.search(
                r"\b\d+(?:\.\d+)?\s*%?\b",
                clean_line
            )

            if year_match:

                current_entry["year"] = (
                    year_match.group(0)
                )

            elif single_year_match:

                current_entry["year"] = (
                    single_year_match.group(0)
                )

            if (
                "cgpa" in clean_line.lower()
                or "%" in clean_line
            ):

                current_entry["score"] = (
                    clean_line
                )

            elif not current_entry["institution"]:

                current_entry["institution"] = (
                    clean_line
                )

    return education


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(sections):

    lines = sections.get(
        "experience",
        []
    )

    experiences = []

    current = None

    for line in lines:

        clean_line = clean_text(line)

        if not clean_line:
            continue

        line_lower = clean_line.lower()

        # Detect internship/job entry
        is_new_entry = (
            "hcl tech" in line_lower
            or "singularium" in line_lower
            or "data analyst" in line_lower
            or "data science intern" in line_lower
            or "intern" in line_lower
            or "freelanc" in line_lower
        )

        if is_new_entry:

            if current:

                experiences.append(
                    current
                )

            current = {
                "title": "",
                "company": "",
                "location": "",
                "duration": ""
            }

            # Remove bullet markers
            clean_line = clean_text(
                clean_line
            )

            # Try to identify company
            if "hcl" in line_lower:

                current["company"] = (
                    "HCL Tech"
                )

            elif "singularium" in line_lower:

                current["company"] = (
                    "Singularium Technologies"
                )

            # Identify title
            if "data science intern" in line_lower:

                current["title"] = (
                    "Data Science Intern"
                )

            elif "data analyst intern" in line_lower:

                current["title"] = (
                    "Data Analyst Intern"
                )

            elif "data analyst" in line_lower:

                current["title"] = (
                    "Data Analyst"
                )

            # Location
            if "noida" in line_lower:

                current["location"] = (
                    "Noida, India"
                )

            elif "bengaluru" in line_lower:

                current["location"] = (
                    "Bengaluru, India"
                )

            continue

        if current:

            # Date range
            date_range = re.search(
                r"(February|January|March|April|May|June|"
                r"July|August|September|October|November|December)"
                r"\s+20\d{2}\s*[-–]\s*"
                r"(February|January|March|April|May|June|"
                r"July|August|September|October|November|December)"
                r"\s+20\d{2}",
                clean_line,
                re.IGNORECASE
            )

            if date_range:

                current["duration"] = (
                    date_range.group(0)
                )

            elif (
                "months" in line_lower
                or "month" in line_lower
            ):

                current["duration"] = (
                    clean_line
                )

            elif (
                "data science intern"
                in line_lower
            ):

                current["title"] = (
                    "Data Science Intern"
                )

            elif (
                "data analyst intern"
                in line_lower
            ):

                current["title"] = (
                    "Data Analyst Intern"
                )

    if current:

        experiences.append(
            current
        )

    return experiences


# ============================================================
# CERTIFICATION / ACHIEVEMENT EXTRACTION
# ============================================================

def extract_certifications(sections):

    lines = sections.get(
        "certifications",
        []
    )

    certifications = []

    for line in lines:

        clean_line = clean_text(line)

        if not clean_line:
            continue

        certifications.append(
            clean_line
        )

    return unique_list(
        certifications
    )


# ============================================================
# TECHNICAL SKILLS
# ============================================================

def extract_structured_skills(sections):

    lines = sections.get(
        "skills",
        []
    )

    skills = []

    for line in lines:

        clean_line = clean_text(line)

        if not clean_line:
            continue

        # Remove common bullet markers
        clean_line = re.sub(
            r"^[•❖▪\-]+\s*",
            "",
            clean_line
        )

        # Split multiple skills if necessary
        parts = re.split(
            r",|;",
            clean_line
        )

        for part in parts:

            part = clean_text(part)

            if part:

                skills.append(
                    part
                )

    return unique_list(
        skills
    )


# ============================================================
# SOFT SKILLS
# ============================================================

def extract_soft_skills(sections):

    lines = sections.get(
        "soft_skills",
        []
    )

    soft_skills = []

    for line in lines:

        clean_line = clean_text(line)

        clean_line = re.sub(
            r"^[•❖▪\-]+\s*",
            "",
            clean_line
        )

        if clean_line:

            soft_skills.append(
                clean_line
            )

    return unique_list(
        soft_skills
    )


# ============================================================
# PROJECT EXTRACTION
# ============================================================

def extract_projects(sections):

    lines = sections.get(
        "projects",
        []
    )

    projects = []

    current_project = None

    for line in lines:

        clean_line = clean_text(line)

        if not clean_line:
            continue

        # Project lines generally begin with bullet
        # in the original resume.
        if (
            "–" in clean_line
            or "-" in clean_line
            or "—" in clean_line
        ):

            parts = re.split(
                r"\s+[–—-]\s+",
                clean_line,
                maxsplit=1
            )

            if len(parts) == 2:

                if current_project:

                    projects.append(
                        current_project
                    )

                current_project = {
                    "name": clean_text(
                        parts[0]
                    ),
                    "description": clean_text(
                        parts[1]
                    )
                }

                continue

        if current_project:

            current_project["description"] += (
                " " + clean_line
            )

    if current_project:

        projects.append(
            current_project
        )

    return projects


# ============================================================
# CONTACT EXTRACTION
# ============================================================

def extract_contact_information(text):

    email = None
    phone = None

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:

        email = email_match.group(
            0
        )

    phone_match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    if phone_match:

        phone = phone_match.group(
            0
        )

    return {
        "email": email,
        "phone": phone
    }


# ============================================================
# MAIN PROFILE BUILDER
# ============================================================

def build_career_profile(
    resume_text,
    skills,
    entities
):

    sections = extract_sections(
        resume_text
    )

    profile = {

        "name": "",

        "profile": extract_profile(
            sections
        ),

        "skills": skills,

        "structured_skills":
            extract_structured_skills(
                sections
            ),

        "soft_skills":
            extract_soft_skills(
                sections
            ),

        "education":
            extract_education(
                sections
            ),

        "experience":
            extract_experience(
                sections
            ),

        "certifications":
            extract_certifications(
                sections
            ),

        "projects":
            extract_projects(
                sections
            ),

        "people": [],

        "organizations": [],

        "locations": [],

        "dates": [],

        "contact":
            extract_contact_information(
                resume_text
            )
    }

    # ========================================================
    # NAME
    # ========================================================

    lines = resume_text.splitlines()

    for line in lines:

        clean_line = clean_text(line)

        if (
            clean_line
            and clean_line.lower()
            not in [
                "curriculum vitae",
                "cv"
            ]
            and len(clean_line.split()) <= 5
        ):

            # The uploaded CV places the candidate name
            # immediately after "Curriculum Vitae".
            if clean_line.upper() == clean_line:
                profile["name"] = clean_line
                break

    # ========================================================
    # SPAcy ENTITY INFORMATION
    # ========================================================

    for entity in entities:

        entity_text = clean_text(
            entity["text"]
        )

        label = entity["label"]

        if label == "PERSON":

            profile["people"].append(
                entity_text
            )

        elif label == "ORG":

            profile["organizations"].append(
                entity_text
            )

        elif label in [
            "GPE",
            "LOC",
            "FAC"
        ]:

            profile["locations"].append(
                entity_text
            )

        elif label in [
            "DATE",
            "CARDINAL"
        ]:

            profile["dates"].append(
                entity_text
            )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    profile["people"] = unique_list(
        profile["people"]
    )

    profile["organizations"] = unique_list(
        profile["organizations"]
    )

    profile["locations"] = unique_list(
        profile["locations"]
    )

    profile["dates"] = unique_list(
        profile["dates"]
    )

    return profile