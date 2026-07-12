# utils/aggregator.py
import os
from datetime import date

from parsers.resume_parser   import extract_resume_text
from parsers.github_parser   import fetch_github_profile, fetch_github_repos
from parsers.linkedin_parser import extract_profile_summary, extract_skills, extract_positions

from utils.text_utils        import clean_resume_data, clean_github_data, clean_linkedin_data

from scorers.resume_scorer   import score_resume
from scorers.github_scorer   import score_github
from scorers.linkedin_scorer import score_linkedin

WEIGHTS = {
    "resume":   0.50,
    "github":   0.20,
    "linkedin": 0.30,
}

def run_pipeline(resume_path, github_username, linkedin_folder):
    """
    Runs the full scoring pipeline and returns a combined report dict.
    """
    # --- parse ---
    resume_raw   = extract_resume_text(resume_path)
    gh_profile   = fetch_github_profile(github_username)
    gh_repos     = fetch_github_repos(github_username)
    li_summary   = extract_profile_summary(linkedin_folder)
    li_skills    = extract_skills(linkedin_folder)
    li_positions = extract_positions(linkedin_folder)

    # --- clean ---
    resume_clean  = clean_resume_data(resume_raw)
    github_clean  = clean_github_data(gh_profile, gh_repos)
    linkedin_clean = clean_linkedin_data(li_summary, li_skills, li_positions)

    # --- score ---
    resume_result   = score_resume(resume_clean)
    github_result   = score_github(github_clean)
    linkedin_result = score_linkedin(linkedin_clean)

    # --- aggregate ---
    weighted_total = (
        resume_result["score"]   * WEIGHTS["resume"]  +
        github_result["score"]   * WEIGHTS["github"]  +
        linkedin_result["score"] * WEIGHTS["linkedin"]
    )

    return {
        "candidate":  linkedin_clean["name"],
        "date":       str(date.today()),
        "scores": {
            "resume":   resume_result["score"],
            "github":   github_result["score"],
            "linkedin": linkedin_result["score"],
            "total":    round(weighted_total, 1),
        },
        "feedback": {
            "resume":   resume_result["feedback"],
            "github":   github_result["feedback"],
            "linkedin": linkedin_result["feedback"],
        }
    }
    
def generate_report(report):
    """
    Takes run_pipeline() output and returns a formatted report string.
    """
    lines = []
    lines.append("=" * 50)
    lines.append("   CAREER PROFILE SCORE REPORT")
    lines.append("=" * 50)
    lines.append(f"Candidate : {report['candidate']}")
    lines.append(f"Date      : {report['date']}")
    lines.append("")

    # scores section"
    scores = report["scores"]
    lines.append(f"RESUME    {scores['resume']}/100  (weight: {WEIGHTS['resume']*100:.0f}%)  → {scores['resume'] * WEIGHTS['resume']:.1f} pts")
    lines.append(f"GITHUB    {scores['github']}/100  (weight: {WEIGHTS['github']*100:.0f}%)  → {scores['github'] * WEIGHTS['github']:.1f} pts")
    lines.append(f"LINKEDIN  {scores['linkedin']}/100  (weight: {WEIGHTS['linkedin']*100:.0f}%)  → {scores['linkedin'] * WEIGHTS['linkedin']:.1f} pts")
    lines.append("-" * 50)
    lines.append(f"TOTAL     {scores['total']}/100")

    # feedback section
    lines.append("")
    lines.append("FEEDBACK")
    for source, items in report["feedback"].items():
        if items:
            lines.append(f"{source.upper()}:")
            for item in items:
                lines.append(f"  - {item}")

    lines.append("=" * 50)
    return "\n".join(lines)

def save_report(report, output_dir="outputs/"):
    """
    Saves the formatted report to a .txt file in outputs/
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"report_{report['candidate'].replace(' ', '_')}_{report['date']}.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(generate_report(report))
    print(f"Report saved to {filepath}")
    return filepath


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    report = run_pipeline(
        resume_path      = r"C:\Users\basil\OneDrive\Documents\personal docs\BasilAnil_Resume.pdf",
        github_username  = "Blitzhac",
        linkedin_folder  = r"C:\Users\basil\Downloads\Basic_LinkedInDataExport_07-07-2026.zip"
    )

    print(generate_report(report))
    save_report(report)