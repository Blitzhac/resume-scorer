# main.py
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.aggregator import run_pipeline, generate_report, save_report

def parse_args():
    parser = argparse.ArgumentParser(
        description="Career Profile Scorer — score your resume, GitHub, and LinkedIn."
    )
    parser.add_argument("--resume",   required=True,  help="Path to resume PDF or DOCX")
    parser.add_argument("--github",   required=True,  help="GitHub username")
    parser.add_argument("--linkedin", required=True,  help="Path to LinkedIn export folder")
    return parser.parse_args()

def main():
    args = parse_args()

    print("Running pipeline...")
    report = run_pipeline(
        resume_path     = args.resume,
        github_username = args.github,
        linkedin_folder = args.linkedin
    )

    print(generate_report(report))
    save_report(report)

if __name__ == "__main__":
    main()