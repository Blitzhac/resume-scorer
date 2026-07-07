# scorers/github_scorer.py

def score_github(cleaned):
    """
    Takes clean_github_data() output and returns score + feedback.
    """
    score    = 0
    feedback = []

    # 1. bio — 10pts
    if cleaned["has_bio"]:
        score += 10
    else:
        feedback.append("Add a bio to your GitHub profile — it helps recruiters understand you.")

    # 2. original repos > 3 — 20pts
    if cleaned["original_repos"] > 3:
        score += 20
    else:
        feedback.append(f"You have {cleaned['original_repos']} original repos. Aim for at least 3 to showcase your work.")

    # 3. total stars > 0 — 10pts
    if cleaned["total_stars"] > 0:
        score += 10
    else:
        feedback.append("Your GitHub profile has 0 total stars. Try contributing to open-source projects to increase your star count.")

    # 4. multiple languages — 10pts
    if len(cleaned["top_languages"]) > 1:
        score += 10
    else:
        feedback.append("Your GitHub profile doesn't show multiple programming languages. Highlight your skills by working on diverse projects.")

    # 5. original repos > 5 — 25pts
    if cleaned["original_repos"] > 5:
        score += 25
    else:
        feedback.append(f"You have {cleaned['original_repos']} original repos. Aim for at least 5 to showcase your work.")

    # 6. has website/portfolio — 25pts
    if cleaned["has_website"]:
        score += 25
    else:
        feedback.append("Add a website or portfolio link to your GitHub profile — it helps recruiters learn more about you.")

    return {
        "score":    score,
        "feedback": feedback
    }

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from parsers.github_parser import fetch_github_profile, fetch_github_repos
    from utils.text_utils import clean_github_data

    profile = fetch_github_profile("Blitzhac")
    repos   = fetch_github_repos("Blitzhac")
    cleaned = clean_github_data(profile, repos)
    result  = score_github(cleaned)

    print(f"GitHub Score: {result['score']}/100")
    print("Feedback:")
    for f in result['feedback']:
        print(f"  - {f}")