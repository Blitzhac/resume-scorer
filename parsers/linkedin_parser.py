# parsers/linkedin_parser.py
import csv
import os

def load_csv(file_path):
    rows = []
    with open(file_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def parse_linkedin_export(export_folder):
    data = {
        "profile":   [],
        "skills":    [],
        "positions": [],
        "education": [],
    }
    file_map = {
        "profile":   "Profile.csv",
        "skills":    "Skills.csv",
        "positions": "Positions.csv",
        "education": "Education.csv",
    }
    for key, filename in file_map.items():
        file_path = os.path.join(export_folder, filename)
        if os.path.exists(file_path):
            data[key] = load_csv(file_path)
        else:
            print(f"Warning: {filename} not found in {export_folder}. Skipping.")
    return data

def extract_profile_summary(export_folder):
    profiles = load_csv(os.path.join(export_folder, "Profile.csv"))
    if not profiles:
        raise ValueError("Profile.csv is empty or could not be read.")
    raw = profiles[0]
    return {
        "first_name": raw["First Name"],
        "last_name":  raw["Last Name"],
        "headline":   raw["Headline"],
        "summary":    raw["Summary"],
        "industry":   raw["Industry"],
        "website":    raw["Websites"],
    }

if __name__ == "__main__":
    folder = r"C:\Users\basil\Downloads\Basic_LinkedInDataExport_07-06-2026.zip"
    data = parse_linkedin_export(folder)
    print(data)
    summary = extract_profile_summary(folder)
    print(summary)