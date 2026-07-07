# utils/text_utils.py
def clean_github_data(profile, repos):
    """
    Takes raw GitHub API dicts and returns only what the scorer needs.
    """
    # from profile dict — these are direct lookups
    public_repos = profile.get("public_repos", 0)
    followers    = profile.get("followers", 0)
    has_bio      = bool(profile.get("bio"))
    has_website  = bool(profile.get("blog"))

    # from repos list — these need loops
    total_stars   = 0
    languages     = []
    original_repos = 0   # repos where fork is False

    for repo in repos:
        total_stars += repo.get("stargazers_count", 0)
        language = repo.get("language")
        if language:
            languages.append(language)
        if not repo.get("fork"):
            original_repos += 1

    return {
        "public_repos":    public_repos,
        "followers":       followers,
        "has_bio":         has_bio,
        "has_website":     has_website,
        "total_stars":     total_stars,
        "top_languages":   list(set(languages)),  # deduplicated
        "original_repos":  original_repos,
    }
    
def clean_linkedin_data(summary):
    """
    Takes extract_profile_summary() output and returns scorer-ready dict.
    """
    return {
        "name":           f"{summary['first_name']} {summary['last_name']}",
        "headline":       summary.get("headline", ""),
        "summary":        summary.get("summary", ""),
        "industry":       summary.get("industry", ""),
        "has_headline":   bool(summary.get("headline")),   # is headline non-empty?
        "has_summary":    bool(summary.get("summary")),    # is summary non-empty?
        "has_website":    bool(summary.get("website")),    # is website non-empty?
        "headline_length": len(summary.get("headline", "")),  # number of characters in headline
        "summary_length":  len(summary.get("summary", "")),  # number of characters in summary
    }

import re

# skills to look for — expand this list to match your field
SKILLS_KEYWORDS = [
    "python", "sql", "power bi", "powerbi", "tableau", "excel",
    "machine learning", "deep learning", "pandas", "numpy",
    "scikit-learn", "sklearn", "tensorflow", "pytorch", "fastapi",
    "docker", "git", "streamlit", "javascript", "html", "css",
    "data analysis", "data visualization", "nlp", "opencv",
    "power query", "dax"
]

SECTION_HEADERS = [
    "experience", "education", "skills", "projects",
    "certifications", "summary", "objective", "achievements"
]

def clean_resume_data(raw_text):
    """
    Takes raw resume text and returns structured dict.
    """
    text_lower = raw_text.lower()

    # 1. extract email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
    email = email_match.group() if email_match else None

    # 2. extract phone
    phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,15}', raw_text)
    phone = phone_match.group() if phone_match else None

    # 3. detect which section headers appear in the resume
    found_sections = []
    for section in SECTION_HEADERS:
        if section in text_lower:   # does section appear in text_lower?
            found_sections.append(section)

    # 4. detect which skills appear in the resume
    found_skills = []
    for skill in SKILLS_KEYWORDS:
        if skill in text_lower:   # does skill appear in text_lower?
            found_skills.append(skill)

    return {
        "email":         email,
        "phone":         phone,
        "sections":      found_sections,
        "skills":        found_skills,
        "skill_count":   len(found_skills),
        "section_count": len(found_sections),
        "has_email":     bool(email),
        "has_phone":     bool(phone),
        "word_count":    len(raw_text.split()),
    }

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from parsers.resume_parser import extract_resume_text

    raw = extract_resume_text(r"C:\Users\basil\OneDrive\Documents\personal docs\BasilAnil_Resume.pdf")
    cleaned = clean_resume_data(raw)
    print(cleaned)