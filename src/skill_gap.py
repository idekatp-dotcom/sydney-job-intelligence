import pandas as pd
import re

# Load skill demand results
df = pd.read_csv("data/processed/jobs_clean.csv")
df = df.dropna(subset=["description"])

# Controlled vocabulary
skills = [
    "python", "sql", "aws", "azure", "gcp",
    "java", "c++", "c#", "javascript",
    "react", "node", "docker", "kubernetes",
    "terraform", "linux", "spark",
    "machine learning", "ai", "data",
    "power bi", "tableau", "excel",
    "git", "devops", "cloud"
]

# Build demand map
all_text = " ".join(df["description"].str.lower())
all_text = re.sub(r'[^a-zA-Z\s]', ' ', all_text)

skill_counts = {}
total_jobs = len(df)

for skill in skills:
    pattern = r"\b" + re.escape(skill) + r"\b"
    matches = re.findall(pattern, all_text)
    skill_counts[skill] = len(matches)

# Convert to percentage demand
skill_demand = {
    skill: (count / total_jobs) * 100
    for skill, count in skill_counts.items()
}

# ---------- USER INPUT ----------
user_skills = ["python", "aws", "sql"]  # change this to test

# ---------- ANALYSIS ----------
alignment_score = 0
missing_high_demand = []
strong_alignment = []

for skill, demand in skill_demand.items():
    if skill in user_skills:
        alignment_score += demand
        strong_alignment.append((skill, round(demand, 2)))
    else:
        if demand > 5:  # threshold for high demand
            missing_high_demand.append((skill, round(demand, 2)))

alignment_score = round(alignment_score, 2)

print("\n--- SKILL GAP ANALYSIS ---\n")
print("User Skills:", user_skills)
print("\nAlignment Score:", alignment_score, "%\n")

print("Strong Market Alignment:")
for skill, demand in strong_alignment:
    print(f"- {skill} ({demand}%)")

print("\nMissing High-Demand Skills:")
for skill, demand in sorted(missing_high_demand, key=lambda x: x[1], reverse=True):
    print(f"- {skill} ({demand}%)")
    