# scorers/resume_scorer.py

def score_resume(cleaned):
    """
    Takes clean_resume_data() output and returns score + feedback.
    """
    score    = 0
    feedback = []

    # 1. email — 10pts
    if cleaned["has_email"]:
        score += 10
    else:
        feedback.append("Add your email address — recruiters need it.")

    # 2. phone — 10pts
    if cleaned["has_phone"]:
        score += 10
    else:
        feedback.append("Add your phone number — it helps recruiters reach you.")

    # 3. sections — 20pts
    if cleaned["section_count"] >= 5:
        score += 20
    else:
        feedback.append(f"Your resume has {cleaned['section_count']} sections. Aim for at least 5: Experience, Education, Skills, Projects, Summary.")

    # 4. skills — 20pts
    if cleaned["skill_count"] > 5:
        score += 20
    else:
        feedback.append(f"Only {cleaned['skill_count']} skills detected. Add more relevant technical skills.")

    # 5. word count — 5pts
    if 300 <= cleaned["word_count"] <= 800:
        score += 5
    else:
        feedback.append(f"Your resume is {cleaned['word_count']} words. Aim for 300–800 words.")

    # 6. projects — 35pts
    if "projects" in cleaned["sections"] and cleaned["skill_count"] > 3:
        score += 35
    else:
        feedback.append("Add a Projects section with specific tools used — it's worth 35 points.")

    return {
        "score":    score,
        "feedback": feedback
    }
    
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from parsers.resume_parser import extract_resume_text
    from utils.text_utils import clean_resume_data

    raw     = extract_resume_text(r"C:\Users\basil\OneDrive\Documents\personal docs\BasilAnil_Resume.pdf")
    cleaned = clean_resume_data(raw)
    result  = score_resume(cleaned)
    print(f"Resume Score: {result['score']}/100")
    print("Feedback:")
    for f in result['feedback']:
        print(f"  - {f}")