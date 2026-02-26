import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Sydney Job Intelligence", layout="centered")

st.title("Sydney Tech Job Market Intelligence")
st.subheader("Skill Gap Analyzer")

# Load dataset
df = pd.read_csv("data/processed/jobs_clean.csv")
df = df.dropna(subset=["description"])

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

total_jobs = len(df)
skill_demand = {}

for skill in skills:
    pattern = r"\b" + re.escape(skill) + r"\b"
    matches = re.findall(pattern, all_text)
    skill_demand[skill] = (len(matches) / total_jobs) * 100

# ---- USER INPUT ----
user_input = st.text_input("Enter your skills (comma separated):")

if user_input:
    user_skills = [s.strip().lower() for s in user_input.split(",")]

    alignment_score = 0
    strong_alignment = []
    missing_high_demand = []

    for skill, demand in skill_demand.items(): 
        if skill in user_skills:
            alignment_score += demand
            strong_alignment.append((skill, round(demand, 2)))
        else:
            if demand > 5:
                missing_high_demand.append((skill, round(demand, 2)))

    alignment_score = round(alignment_score, 2)

    st.markdown("## Results")
    st.metric("Market Alignment Score", f"{alignment_score}%")

    st.markdown("### Strong Market Alignment")
    for skill, demand in strong_alignment:
        st.write(f"✔ {skill} ({demand}%)")

    st.markdown("### Missing High-Demand Skills")
    for skill, demand in sorted(missing_high_demand, key=lambda x: x[1], reverse=True):
        st.write(f"⚠ {skill} ({demand}%)")