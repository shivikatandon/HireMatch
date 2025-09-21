from pathlib import Path

def normalize_text(t: str) -> str:
    return " ".join(t.split()).lower()

def load_skills_list(path="skills_master.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

def extract_jd_skills(jd_text: str, skills_master: set) -> set:
    j = normalize_text(jd_text)
    found = set()
    for skill in skills_master:
        if skill in j:
            found.add(skill)
    return found

if __name__ == "__main__":
    skills_master = load_skills_list("skills_master.txt")

    jd_folder = Path("sample_data")
    print("Looking for JD files in:", jd_folder.resolve())
    for jd_file in jd_folder.glob("jobdes*.txt"):
        print(f"\n📄 Found file: {jd_file.name}")
        jd_text = jd_file.read_text(encoding="utf-8")
        print("Raw JD preview:", jd_text[:200], "...\n")  # show first 200 chars
        found_skills = extract_jd_skills(jd_text, skills_master)
        print("JD Skills required:", ", ".join(found_skills) if found_skills else "No skills detected")
