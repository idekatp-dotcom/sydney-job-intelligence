import pandas as pd
import re
from collections import Counter

# Load dataset
df = pd.read_csv("data/processed/jobs_clean.csv")

df = df.dropna(subset=["description"])

# Combine all descriptions into one big text blob
all_text = " ".join(df["description"].str.lower())

# Clean text
all_text = re.sub(r'[^a-zA-Z\s]', ' ', all_text)

# Define technical skill keywords
skills = [
    "python", "sql", "aws", "azure", "gcp",
    "java", "c++", "c#", "javascript",
    "react", "node", "docker", "kubernetes",
    "terraform", "linux", "spark",
    "machine learning", "ai", "data",
    "power bi", "tableau", "excel",
    "git", "devops", "cloud"
]

# Count occurrences
skill_counts = {}

for skill in skills:
    pattern = r"\b" + re.escape(skill) + r"\b"
    matches = re.findall(pattern, all_text)
    skill_counts[skill] = len(matches)

# Sort by frequency
sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)

total_jobs = len(df)

print("\nTop Technical Skills in Sydney Engineering Jobs:\n")

for skill, count in sorted_skills:
    percentage = (count / total_jobs) * 100
    print(f"{skill}: {count} jobs ({percentage:.2f}%)")
    
