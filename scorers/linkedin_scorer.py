# scorers/linkedin_scorer.py

def score_linkedin(cleaned):
    score    = 0
    feedback = []

    # 1. has_headline — 10pts
    if cleaned["has_headline"]:
        score += 10
    else:
        feedback.append("Add a headline to your LinkedIn profile.")

    # 2. has_summary — 10pts
    if cleaned["has_summary"]:
        score += 10
    else:
        feedback.append("Add a summary to your LinkedIn profile.")

    # 3. headline_length > 100 — 5pts
    if cleaned["headline_length"] > 100:
        score += 5
    else:
        feedback.append("Your headline is too short — make it more descriptive.")

    # 4. summary_length > 500 — 5pts
    if cleaned["summary_length"] > 500:
        score += 5
    else:
        feedback.append("Your summary is too short — expand on your background.")

    # 5. has_website — 10pts
    if cleaned["has_website"]:
        score += 10
    else:
        feedback.append("Add a portfolio or website link to your LinkedIn profile.")

    # 6. industry filled — 10pts
    if cleaned["industry"]:
        score += 10
    else:
        feedback.append("Fill in your industry on LinkedIn.")

    # 7. skills — 20pts (NOW UNLOCKED)
    if cleaned["skill_count"] >= 5:
        score += 20
    elif cleaned["skill_count"] >= 3:
        score += 10
    else:
        feedback.append("Add more skills to your LinkedIn profile.")

    # 8. experience — 10pts (NOW UNLOCKED)
    if cleaned["has_experience"]:
        score += 10
    else:
        feedback.append("Add work experience to your LinkedIn profile.")
    # your turn: check has_experience, award points, append feedback if missing

    # TODO: connections → 10pts (still needs Connections.csv parsing)

    return {
        "score":    score,
        "feedback": feedback
    }
    
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from parsers.linkedin_parser import (
        extract_profile_summary,
        extract_skills,
        extract_positions
    )
    from utils.text_utils import clean_linkedin_data

    folder   = r"C:\Users\basil\Downloads\Basic_LinkedInDataExport_07-07-2026.zip"
    summary  = extract_profile_summary(folder)
    skills   = extract_skills(folder)
    positions = extract_positions(folder)
    cleaned  = clean_linkedin_data(summary, skills, positions)

    print(f"Skills found: {cleaned['skill_count']}")
    print(f"Positions found: {cleaned['position_count']}")
    print(f"Current role: {cleaned['current_role']}")
    print()

    result = score_linkedin(cleaned)
    print(f"LinkedIn Score: {result['score']}/100")
    print("Feedback:")
    for f in result['feedback']:
        print(f"  - {f}")