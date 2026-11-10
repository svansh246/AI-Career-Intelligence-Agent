import streamlit as st
import json
import pandas as pd
from datetime import datetime

from resume_parser import extract_resume_text
from skills_database import extract_skills
from career_profile import build_career_profile
from career_domain import detect_career_domain
from skill_gap import analyze_skill_gap
from career_recommendations import get_career_recommendations
from career_roadmap import generate_roadmap
from career_readiness import evaluate_readiness, readiness_label
from job_analyzer import analyze_job_description
from matching_engine import match_resume_to_job
from personalized_learning import generate_learning_plan
from learning_resources import get_learning_resources
from resume_improver import generate_resume_review

from database import (
    initialize_database,
    save_analysis,
    get_analysis_history,
    get_analysis_by_id,
    delete_analysis,
    clear_analysis_history,
)


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Career Intelligence Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "profile": None,
    "skills": [],
    "domains": [],
    "primary_domain": None,
    "resume_text": "",
    "resume_filename": "",
    "job_analysis": None,
    "job_match": None,
    "resume_review": None,
    "learning_progress": {},
    "history_confirm_clear": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================

def safe_entities(text):
    """Run optional NLP entity extraction without breaking the app."""
    try:
        import nlp_analyzer

        for function_name in (
            "extract_entities",
            "get_entities",
            "analyze_entities",
            "extract_named_entities",
        ):
            function = getattr(nlp_analyzer, function_name, None)
            if callable(function):
                result = function(text)
                return result or {}

    except Exception as error:
        st.warning(f"Optional NLP entity extraction skipped: {error}")

    return {}


def primary_domain():
    domain = st.session_state.primary_domain
    if domain:
        return domain

    domains = st.session_state.domains
    if domains:
        first = domains[0]
        return first[0] if isinstance(first, (tuple, list)) else str(first)

    return "AI / Machine Learning"


def normalize_domain_items(domains):
    """Convert domain results into displayable (name, score) pairs."""
    output = []
    for item in domains or []:
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            output.append((str(item[0]), item[1]))
        else:
            output.append((str(item), None))
    return output


def show_skills(skills):
    if not skills:
        st.info("No skills detected.")
        return

    st.write(" · ".join(str(skill) for skill in skills))


def require_profile():
    if not st.session_state.profile:
        st.warning("Please upload and analyze your resume first.")
        st.info("Go to **Resume Analyzer** to begin.")
        return False
    return True


def render_resources(skills):
    st.subheader("📚 Free Learning Resources")

    if not skills:
        st.info("No missing skills to display resources for.")
        return

    for skill in skills:
        with st.expander(f"Resources for {skill}"):
            try:
                resources = get_learning_resources(skill) or []

                if isinstance(resources, dict):
                    resources = [resources]

                if not resources:
                    st.write("No resource entries found.")
                    continue

                for resource in resources:
                    if not isinstance(resource, dict):
                        st.write(str(resource))
                        continue

                    name = resource.get("name", "Learning resource")
                    url = resource.get("url", "")
                    kind = resource.get("type", "Resource")
                    description = resource.get("description", "")

                    if url:
                        st.markdown(f"**[{name}]({url})** — {kind}")
                    else:
                        st.markdown(f"**{name}** — {kind}")

                    if description:
                        st.caption(description)

            except Exception as error:
                st.error(f"Could not load resources: {error}")


def calculate_current_gap():
    """Get the current skill-gap result using the selected career domain."""
    return analyze_skill_gap(
        st.session_state.skills,
        primary_domain(),
    )


def get_readiness(gap):
    return evaluate_readiness(
        st.session_state.profile,
        st.session_state.skills,
        gap,
        primary_domain(),
    )


def safe_score(value):
    try:
        return max(0, min(100, float(value)))
    except (TypeError, ValueError):
        return 0


def show_readiness(readiness):
    if not isinstance(readiness, dict):
        st.warning("Readiness result is not in the expected format.")
        st.write(readiness)
        return

    score = safe_score(readiness.get("overall", 0))
    st.metric("Career readiness indicator", f"{score:.0f}/100")
    st.progress(score / 100)

    try:
        st.caption(readiness_label(score))
    except Exception:
        st.caption("Heuristic indicator based on the current profile.")

    st.caption(
        "This is an informational checklist indicator, not a hiring "
        "prediction, validated assessment, or guarantee of employability."
    )


def display_dict_items(items, title_key="title"):
    if not items:
        st.info("No items available.")
        return

    if isinstance(items, dict):
        items = list(items.items())

    for item in items:
        if isinstance(item, dict):
            title = (
                item.get(title_key)
                or item.get("name")
                or item.get("topic")
                or "Item"
            )
            with st.expander(str(title)):
                for key, value in item.items():
                    if key == title_key:
                        continue
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")

        elif isinstance(item, (tuple, list)) and len(item) == 2:
            st.write(f"**{item[0]}:** {item[1]}")

        else:
            st.write(str(item))


def json_download(data, filename):
    content = json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
        default=str,
    )

    st.download_button(
        "Download JSON",
        data=content,
        file_name=filename,
        mime="application/json",
    )


# =========================================================
# STYLE AND HEADER
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.15rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    .subtitle {
        color: #888;
        margin-bottom: 1.2rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 12px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🚀 AI Career Intelligence Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Resume analysis • Career guidance • Skill gaps • '
    'Job matching • Learning roadmap</div>',
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

PAGES = [
    "Dashboard",
    "Resume Analyzer",
    "Resume Improvement",
    "Career Intelligence",
    "Career Roadmap",
    "Career Readiness",
    "Job Description Matcher",
    "Personalized Learning Plan",
    "Analysis History",
]

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Choose a section", PAGES)

st.sidebar.divider()

if st.session_state.profile:
    st.sidebar.success("Resume analyzed")

    st.sidebar.write(
        f"**Name:** {st.session_state.profile.get('name', 'Not detected')}"
    )

    st.sidebar.write(
        f"**Skills:** {len(st.session_state.skills)} detected"
    )

    st.sidebar.write(
        f"**Career domain:** {primary_domain()}"
    )

else:
    st.sidebar.info("Upload a resume to begin")


if st.sidebar.button("Reset current session", use_container_width=True):
    for key, value in DEFAULTS.items():
        st.session_state[key] = value

    st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    if not st.session_state.profile:

        st.write(
            "Welcome! Upload your resume to explore your skills, career "
            "directions, job matching, and learning roadmap."
        )

        if st.button("Go to Resume Analyzer", type="primary"):
            st.session_state["dashboard_go_upload"] = True
            st.rerun()

    else:

        profile = st.session_state.profile
        skills = st.session_state.skills

        col1, col2, col3 = st.columns(3)

        col1.metric("Detected skills", len(skills))
        col2.metric("Career direction", primary_domain())

        col3.metric(
            "Resume file",
            st.session_state.resume_filename or "Uploaded",
        )

        st.subheader("Profile overview")

        st.write(f"**Name:** {profile.get('name', 'Not detected')}")

        st.write(
            f"**Email:** "
            f"{profile.get('contact', {}).get('email', 'Not detected')}"
        )

        st.write(
            f"**Phone:** "
            f"{profile.get('contact', {}).get('phone', 'Not detected')}"
        )

        st.write(profile.get("profile", "No profile summary detected."))

        st.subheader("Detected skills")
        show_skills(skills)

        st.subheader("Career domain analysis")

        for name, score in normalize_domain_items(
            st.session_state.domains
        ):
            if score is not None:
                st.write(f"**{name}:** {score}")
            else:
                st.write(f"**{name}**")

        st.caption(
            "Career suggestions are based on detected information and "
            "heuristic rules. Review the results before acting on them."
        )


# =========================================================
# 1. RESUME ANALYZER
# =========================================================

elif page == "Resume Analyzer":

    st.header("📄 Resume Analyzer")

    st.write(
        "Upload a PDF, DOCX, or TXT resume to extract information "
        "and identify skills."
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        key="resume_upload",
    )

    if uploaded_file:

        st.info(f"Selected file: {uploaded_file.name}")

        if st.button("Analyze Resume", type="primary"):

            try:
                with st.spinner("Extracting and analyzing your resume..."):

                    resume_text = extract_resume_text(uploaded_file)

                    if not resume_text or not str(resume_text).strip():

                        st.error(
                            "No readable text was found. If this is a scanned "
                            "PDF, text extraction may require OCR."
                        )

                    else:

                        skills = extract_skills(resume_text) or []
                        entities = safe_entities(resume_text)

                        profile = build_career_profile(
                            resume_text,
                            skills,
                            entities,
                        ) or {}

                        domains = detect_career_domain(skills) or []
                        normalized = normalize_domain_items(domains)

                        st.session_state.resume_text = resume_text
                        st.session_state.resume_filename = uploaded_file.name
                        st.session_state.skills = skills
                        st.session_state.profile = profile
                        st.session_state.domains = domains

                        st.session_state.primary_domain = (
                            normalized[0][0]
                            if normalized
                            else "AI / Machine Learning"
                        )

                        st.session_state.job_analysis = None
                        st.session_state.job_match = None
                        st.session_state.resume_review = None
                        st.session_state.learning_progress = {}

                        st.success("Resume analyzed successfully!")

            except Exception as error:
                st.error(f"Resume analysis failed: {error}")

    if st.session_state.profile:

        profile = st.session_state.profile
        contact = profile.get("contact", {}) or {}

        st.divider()
        st.subheader("👤 Extracted Profile")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Name:** {profile.get('name', 'Not detected')}")
            st.write(f"**Email:** {contact.get('email', 'Not detected')}")
            st.write(f"**Phone:** {contact.get('phone', 'Not detected')}")

        with col2:

            st.write(f"**Primary domain:** {primary_domain()}")

            st.write(
                f"**Profile summary:** "
                f"{profile.get('profile', 'Not available')}"
            )

        st.subheader("🧠 Technical Skills")
        show_skills(st.session_state.skills)

        st.subheader("💾 Save this analysis")

        st.caption(
            "Saved records are stored locally in career_assistant.db. "
            "Avoid saving resumes containing information you do not want "
            "stored on this computer."
        )

        default_name = str(profile.get("name") or "")

        save_name = st.text_input(
            "Candidate name / label",
            value=default_name,
            key="analysis_save_name",
        )

        if st.button("Save Analysis to History", type="primary"):

            try:
                gap = calculate_current_gap()
                readiness = get_readiness(gap)

                readiness_score = (
                    readiness.get("overall", 0)
                    if isinstance(readiness, dict)
                    else 0
                )

                record_id = save_analysis(
                    user_name=save_name.strip() or "Unnamed candidate",
                    resume_name=st.session_state.resume_filename,
                    target_domain=primary_domain(),
                    readiness_score=safe_score(readiness_score),
                    skills=st.session_state.skills,
                    profile=st.session_state.profile,
                )

                st.success(f"Analysis saved. Record ID: {record_id}")

            except Exception as error:
                st.error(f"Could not save analysis: {error}")


# =========================================================
# 2. RESUME IMPROVEMENT
# =========================================================

elif page == "Resume Improvement":

    st.header("✨ Resume Improvement Assistant")

    if require_profile():

        profile = st.session_state.profile
        skills = st.session_state.skills
        resume_text = st.session_state.resume_text
        domain = primary_domain()

        st.info(f"Reviewing your resume for: {domain}")

        if st.button("Generate Resume Review", type="primary"):

            try:
                with st.spinner("Reviewing resume sections..."):

                    review = generate_resume_review(
                        resume_text,
                        profile,
                        skills,
                        domain,
                    )

                    st.session_state.resume_review = review or {}

                st.success("Resume review generated.")

            except Exception as error:
                st.error(f"Resume review failed: {error}")

        review = st.session_state.resume_review

        if review:

            completeness = safe_score(
                review.get("completeness_indicator", 0)
            )

            st.subheader("📊 Section coverage")
            st.metric("Detected section coverage", f"{completeness:.0f}%")
            st.progress(completeness / 100)

            st.caption(
                "This is section coverage only. It is not an ATS score "
                "or a validated measure of resume quality."
            )

            st.subheader("🔍 Section-by-section review")

            checks = review.get("checks", {}) or {}

            if isinstance(checks, dict):

                for section, result in checks.items():

                    if isinstance(result, dict):
                        status = result.get("status", "Review")
                        suggestion = result.get("suggestion", "")

                    else:
                        status = "Review"
                        suggestion = str(result)

                    with st.expander(f"{section} — {status}"):
                        st.write(suggestion)

            st.subheader("🎯 Prioritized improvements")

            priorities = review.get("priorities", []) or []

            if priorities:

                for item in priorities:

                    if isinstance(item, dict):

                        priority = item.get("priority", "Suggestion")
                        section = item.get("section", "Resume")
                        suggestion = item.get("suggestion", "")

                        st.markdown(f"**{priority}: {section}**")
                        st.write(suggestion)

                    else:
                        st.write(str(item))

            else:
                st.success(
                    "No flagged sections were returned by these checks."
                )

            st.subheader("📝 Current profile summary")
            st.write(profile.get("profile", "No summary detected."))

            st.info(
                review.get(
                    "note",
                    "Keep all resume statements accurate and verifiable.",
                )
            )

            json_download(review, "resume_review.json")


# =========================================================
# 3. CAREER INTELLIGENCE
# =========================================================

elif page == "Career Intelligence":

    st.header("🧠 Career Intelligence")

    if require_profile():

        skills = st.session_state.skills
        domains = normalize_domain_items(st.session_state.domains)

        st.subheader("Career domain analysis")

        if domains:

            for name, score in domains:

                if score is not None:
                    st.write(f"**{name}** — score: {score}")

                else:
                    st.write(f"**{name}**")

        else:
            st.info("No domain scores generated.")

        domain = primary_domain()

        st.success(f"Primary career direction: {domain}")

        st.subheader("Potential roles and recommendations")

        try:
            recommendations = get_career_recommendations(domain)
            display_dict_items(recommendations, "title")

        except Exception as error:
            st.error(f"Could not load recommendations: {error}")

        # =====================================
        # SKILL GAP ANALYSIS
        # =====================================

        st.subheader("Skill Gap Analysis")

        try:

            gap = analyze_skill_gap(skills, domain) or {}

            matched = gap.get("matched", []) or []
            missing = gap.get("missing", []) or []

            percentage = safe_score(
                gap.get("percentage", 0)
            )

            # Overall skill match percentage

            st.metric(
                "Overall Skill Match",
                f"{percentage:.0f}%"
            )

            st.progress(percentage / 100)

            st.divider()

            # Matched and missing skills

            matched_col, missing_col = st.columns(2)

            with matched_col:

                st.markdown("### ✅ Matched Skills")

                if matched:

                    for skill in matched:
                        st.success(str(skill))

                else:
                    st.info("No matched skills found.")

            with missing_col:

                st.markdown("### ❌ Missing Skills")

                if missing:

                    for skill in missing:
                        st.error(str(skill))

                else:
                    st.success("No missing skills identified.")

            st.divider()

            # Skill summary

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            summary_col1.metric(
                "Matched",
                len(matched)
            )

            summary_col2.metric(
                "Missing",
                len(missing)
            )

            summary_col3.metric(
                "Total Skills",
                len(matched) + len(missing)
            )

            # Recommended skills

            if missing:

                st.subheader("Recommended Skills to Learn")

                st.write(
                    "Focus on developing the following skills to strengthen "
                    "your profile for this career direction:"
                )

                for skill in missing:
                    st.write(f"📚 {skill}")

            else:
                st.success(
                    "Your profile matches all skills identified for this domain."
                )

            json_download(
                gap,
                "career_skill_gap.json"
            )

        except Exception as error:
            st.error(f"Skill-gap analysis failed: {error}")


# =========================================================
# 4. CAREER ROADMAP
# =========================================================

elif page == "Career Roadmap":

    st.header("🗺️ Career Roadmap")

    if require_profile():

        domain = primary_domain()

        st.write(f"Suggested direction: **{domain}**")

        try:

            gap = analyze_skill_gap(
                st.session_state.skills,
                domain,
            ) or {}

            missing = gap.get("missing", [])

            st.subheader("Skills to work on")
            show_skills(missing)

            if st.button("Generate Career Roadmap", type="primary"):

                roadmap = generate_roadmap(domain, missing)

                st.session_state["current_roadmap"] = roadmap

            roadmap = st.session_state.get("current_roadmap")

            if roadmap:

                st.subheader("Your roadmap")

                display_dict_items(roadmap)

                json_download(
                    roadmap,
                    "career_roadmap.json"
                )

        except Exception as error:
            st.error(f"Could not generate roadmap: {error}")


# =========================================================
# 5. CAREER READINESS
# =========================================================

elif page == "Career Readiness":

    st.header("📈 Career Readiness")

    if require_profile():

        try:

            gap = calculate_current_gap()
            readiness = get_readiness(gap)

            show_readiness(readiness)

            if isinstance(readiness, dict):

                st.subheader("Readiness categories")

                categories = readiness.get("categories", {}) or {}

                if isinstance(categories, dict):

                    for name, value in categories.items():

                        st.write(
                            f"**{name.replace('_', ' ').title()}:** {value}"
                        )

                st.subheader("Suggested areas for improvement")

                improvements = readiness.get(
                    "improvement_areas",
                    []
                ) or []

                if improvements:

                    for item in improvements:
                        st.write(f"- {item}")

                else:
                    st.info("No improvement areas were returned.")

                st.subheader("Skill gap")
                st.json(gap)

                json_download(
                    readiness,
                    "career_readiness.json"
                )

        except Exception as error:
            st.error(f"Readiness evaluation failed: {error}")


# =========================================================
# 6. JOB DESCRIPTION MATCHER
# =========================================================

elif page == "Job Description Matcher":

    st.header("🎯 Job Description Matcher")

    if require_profile():

        st.write(
            "Paste a job description to compare its stated skills "
            "with the skills detected in your resume."
        )

        job_text = st.text_area(
            "Paste job description",
            height=260,
            placeholder=(
                "Paste the responsibilities, requirements, "
                "qualifications, and skills from the job posting..."
            ),
            key="job_description_input",
        )

        if st.button("Analyze Job Match", type="primary"):

            if not job_text.strip():

                st.warning("Please paste a job description first.")

            else:

                try:

                    with st.spinner("Analyzing job requirements..."):

                        analysis = analyze_job_description(
                            job_text,
                            st.session_state.skills,
                        )

                        match = match_resume_to_job(
                            st.session_state.resume_text,
                            job_text,
                            st.session_state.skills,
                        )

                        st.session_state.job_analysis = analysis
                        st.session_state.job_match = match

                    st.success("Job description analyzed.")

                except Exception as error:
                    st.error(f"Job matching failed: {error}")

        analysis = st.session_state.job_analysis
        match = st.session_state.job_match

        if analysis:

            st.divider()
            st.subheader("Job requirements")

            st.markdown("**Detected job skills**")
            show_skills(analysis.get("job_skills", []))

            st.markdown("**Skills found in your resume**")
            show_skills(analysis.get("matched", []))

            st.markdown("**Skills not detected in your resume**")
            show_skills(analysis.get("missing", []))

            percentage = safe_score(
                analysis.get("match_percentage", 0)
            )

            st.metric("Skill overlap", f"{percentage:.0f}%")
            st.progress(percentage / 100)

            st.caption(
                "Skill overlap is a keyword-based indicator. It does not "
                "measure your actual proficiency or guarantee job suitability."
            )

            if match is not None:

                st.subheader("Matching engine output")

                if isinstance(match, dict):

                    st.json(match)

                    json_download(
                        match,
                        "job_match.json"
                    )

                else:
                    st.write(match)

            st.subheader("Required skills")
            show_skills(analysis.get("required_lines", []))

            st.subheader("Preferred skills")
            show_skills(analysis.get("preferred_lines", []))


# =========================================================
# 7. PERSONALIZED LEARNING PLAN
# =========================================================

elif page == "Personalized Learning Plan":

    st.header("📚 Personalized Learning Plan")

    if require_profile():

        domain = primary_domain()

        try:

            gap = analyze_skill_gap(
                st.session_state.skills,
                domain,
            ) or {}

            missing = gap.get("missing", [])

            st.write(f"Target direction: **{domain}**")

            st.subheader("Recommended skills to learn")
            show_skills(missing)

            if st.button("Create My Learning Plan", type="primary"):

                plan = generate_learning_plan(domain, missing)

                st.session_state["current_learning_plan"] = plan or []

            plan = st.session_state.get("current_learning_plan")

            if plan:

                st.divider()
                st.subheader("Your learning plan")

                for index, stage in enumerate(plan):

                    if isinstance(stage, dict):

                        title = (
                            stage.get("topic")
                            or stage.get("title")
                            or stage.get("stage")
                            or f"Stage {index + 1}"
                        )

                        with st.expander(
                            str(title),
                            expanded=index == 0
                        ):

                            for key, value in stage.items():

                                if key in ("topic", "title", "stage"):
                                    continue

                                st.write(
                                    f"**{key.replace('_', ' ').title()}:** {value}"
                                )

                            completed_key = f"learning_stage_{index}"

                            completed = st.checkbox(
                                "Mark this stage complete",
                                key=completed_key,
                                value=st.session_state.learning_progress.get(
                                    completed_key,
                                    False
                                ),
                            )

                            st.session_state.learning_progress[
                                completed_key
                            ] = completed

                    else:
                        st.write(f"{index + 1}. {stage}")

                completed_count = sum(
                    bool(value)
                    for value in st.session_state.learning_progress.values()
                )

                st.metric(
                    "Completed stages",
                    f"{completed_count}/{len(plan)}",
                )

                st.progress(
                    completed_count / len(plan) if len(plan) else 0
                )

                json_download(
                    plan,
                    "personalized_learning_plan.json"
                )

            st.divider()

            render_resources(missing)

        except Exception as error:
            st.error(f"Learning plan failed: {error}")


# =========================================================
# 8. ANALYSIS HISTORY
# =========================================================

elif page == "Analysis History":

    st.header("🗃️ Analysis History")

    st.write(
        "View and manage analyses saved on this computer. "
        "The history is stored in your local SQLite database."
    )

    try:

        history = get_analysis_history(limit=100) or []

    except Exception as error:

        history = []

        st.error(f"Could not load history: {error}")

    if not history:

        st.info("No saved analyses yet.")

        st.write(
            "Analyze a resume and use **Save Analysis to History** "
            "to create your first record."
        )

    else:

        st.metric("Saved analyses shown", len(history))

        for item in history:

            record_id = item.get("id")
            title = item.get("user_name") or "Unnamed candidate"
            domain = item.get("target_domain") or "Not specified"
            created = item.get("created_at") or "Date unavailable"
            filename = item.get("resume_name") or "Unknown file"

            score = safe_score(
                item.get("readiness_score", 0)
            )

            with st.expander(
                f"#{record_id} — {title} | {domain} | {created}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(f"**Resume file:** {filename}")
                    st.write(f"**Career domain:** {domain}")

                with col2:

                    st.metric(
                        "Readiness indicator",
                        f"{score:.0f}/100",
                    )

                st.markdown("**Detected skills**")
                show_skills(item.get("skills", []))

                st.markdown("**Saved profile details**")
                st.json(item.get("profile", {}))

                if st.button(
                    "Delete this record",
                    key=f"delete_analysis_{record_id}",
                ):

                    try:

                        delete_analysis(record_id)

                        st.success("Record deleted.")

                        st.rerun()

                    except Exception as error:
                        st.error(f"Could not delete record: {error}")

                if st.button(
                    "Load this analysis into current session",
                    key=f"load_analysis_{record_id}",
                ):

                    try:

                        saved = get_analysis_by_id(record_id)

                        if saved:

                            st.session_state.profile = saved.get(
                                "profile",
                                {}
                            )

                            st.session_state.skills = saved.get(
                                "skills",
                                []
                            )

                            st.session_state.resume_filename = saved.get(
                                "resume_name",
                                ""
                            )

                            st.session_state.primary_domain = saved.get(
                                "target_domain",
                                None
                            )

                            st.session_state.domains = [
                                (st.session_state.primary_domain, 0)
                            ] if st.session_state.primary_domain else []

                            st.session_state.resume_text = ""
                            st.session_state.job_analysis = None
                            st.session_state.job_match = None
                            st.session_state.resume_review = None

                            st.success(
                                "Saved profile loaded. Original resume text "
                                "is not stored in history."
                            )

                            st.rerun()

                        else:
                            st.warning("That record could not be found.")

                    except Exception as error:
                        st.error(f"Could not load record: {error}")

        st.divider()
        st.subheader("Delete history")

        if st.button("Delete All Analysis History"):

            st.session_state.history_confirm_clear = True

        if st.session_state.history_confirm_clear:

            st.warning(
                "This permanently deletes all saved analysis records "
                "from the local database."
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:

                if st.button("Confirm Delete All", type="primary"):

                    try:

                        clear_analysis_history()

                        st.session_state.history_confirm_clear = False

                        st.success("All history deleted.")

                        st.rerun()

                    except Exception as error:
                        st.error(f"Could not clear history: {error}")

            with cancel_col:

                if st.button("Cancel"):

                    st.session_state.history_confirm_clear = False

                    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Career Intelligence Assistant | Local prototype | "
    "Career guidance is informational and should be reviewed."
)