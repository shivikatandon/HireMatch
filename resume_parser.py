from pathlib import Path

def normalize_text(t: str) -> str:
    """Convert text to lowercase and remove extra spaces"""
    return " ".join(t.split()).lower()

def load_skills_list(path="skills_master.txt"):
    """Load master skills list from file"""
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

def extract_resume_skills(resume_text: str, skills_master: set) -> set:
    """Check which skills from master list appear in resume"""
    r = normalize_text(resume_text)
    found = set()
    for skill in skills_master:
        if skill in r:
            found.add(skill)
    return found

if __name__ == "__main__":
    skills_master = load_skills_list("skills_master.txt")

    resume_folder = Path("sample_data")
    for resume_file in resume_folder.glob("resume*.txt"):
        resume_text = resume_file.read_text(encoding="utf-8")
        found_skills = extract_resume_skills(resume_text, skills_master)
        print(f"\n📄 {resume_file.name}")
        print("Skills found:", ", ".join(found_skills) if found_skills else "No skills detected")
