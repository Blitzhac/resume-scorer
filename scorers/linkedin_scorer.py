# scorers/linkedin_scorer.py

def score_linkedin(cleaned):
    score    = 0
    feedback = []

    # 1. has_headline — 10pts
    if cleaned["has_headline"]:
        score += 10
    else:
        feedback.append("Add a headline to your LinkedIn profile — it helps recruiters understand you.")
    # 2. has_summary — 10pts
    if cleaned["has_summary"]:
        score += 10
    else:
        feedback.append("Add a summary to your LinkedIn profile — it gives recruiters insight into your background and goals.")
    # 3. headline_length > 100 — 5pts
    if cleaned["headline_length"] > 100:
        score += 5
    else:
        feedback.append("Your LinkedIn headline is too short. Make it more descriptive.")
    # 4. summary_length > 500 — 5pts
    if cleaned["summary_length"] > 500:
        score += 5
    else:
        feedback.append("Your LinkedIn summary is too short. Expand on your background and goals.")
    # 5. has_website — 10pts
    if cleaned["has_website"]:
        score += 10
    else:
        feedback.append("Add a website or portfolio link to your LinkedIn profile — it helps recruiters learn more about you.")
    # 6. industry filled — 10pts
    if cleaned["industry"]:
        score += 10
    else:
        feedback.append("Fill in your industry on your LinkedIn profile — it helps recruiters understand your field.")
    # TODO: skills → 20pts (needs full LinkedIn export)
    # TODO: connections → 10pts (needs full LinkedIn export)  
    # TODO: posts → 10pts (needs full LinkedIn export)
    # current max score until full export: 50pts

    return {
        "score":    score,
        "feedback": feedback
    }
    
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from parsers.linkedin_parser import extract_profile_summary
    from utils.text_utils import clean_linkedin_data

    summary = extract_profile_summary(r"C:\Users\basil\Downloads\Basic_LinkedInDataExport_07-06-2026.zip")
    cleaned = clean_linkedin_data(summary)
    result  = score_linkedin(cleaned)

    print(f"LinkedIn Score: {result['score']}/100")
    print("Feedback:")
    for f in result['feedback']:
        print(f"  - {f}")