from pathlib import Path
from jd_parser import load_skills_list, extract_jd_skills
from resume_parser import extract_resume_skills

def compare_resume_to_jd(resume_skills, jd_skills):
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0
    return matched, missing, score

if __name__ == "__main__":
    # Load skills
    skills_master = load_skills_list("skills_master.txt")

    # Pick JD file (change this to jobdes2.txt if you want)
    jd_file = Path("sample_data/jobdes1.txt")
    jd_text = jd_file.read_text(encoding="utf-8")
    jd_skills = extract_jd_skills(jd_text, skills_master)

    print(f"📄 Comparing resumes against: {jd_file.name}")
    print(f"JD Skills: {', '.join(jd_skills)}\n")

    # Loop through resumes
    resume_folder = Path("sample_data")
    for resume_file in resume_folder.glob("resume*.txt"):
        resume_text = resume_file.read_text(encoding="utf-8")
        resume_skills = extract_resume_skills(resume_text, skills_master)

        matched, missing, score = compare_resume_to_jd(resume_skills, jd_skills)

        print(f"👤 {resume_file.name}")
        print(f"   Matched Skills: {', '.join(matched) if matched else 'None'}")
        print(f"   Missing Skills: {', '.join(missing) if missing else 'None'}")
        print(f"   Relevance Score: {score}%\n")
