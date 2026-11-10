
from database import (
    initialize_database,
    save_analysis,
    get_analysis_history,
    get_analysis_by_id,
    delete_analysis
)

initialize_database()

test_id = save_analysis(
    user_name="Test User",
    resume_name="sample_resume.pdf",
    target_domain="AI / Machine Learning",
    readiness_score=72,
    skills=["Python", "Machine Learning", "Pandas"],
    profile={"education": ["B.Tech"], "projects": ["AI project"]}
)

print("Saved analysis ID:", test_id)

history = get_analysis_history()
print("History:", history)

record = get_analysis_by_id(test_id)
print("Loaded record:", record)

delete_analysis(test_id)
print("Test record deleted.")