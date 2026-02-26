import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def fetch_jobs(pages=10):
    all_jobs = []

    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")

        url = f"https://api.adzuna.com/v1/api/jobs/au/search/{page}"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 50,
            "what": "engineer",
            "where": "NSW"
        }

        response = requests.get(url, params=params)
        data = response.json()

        jobs = data.get("results", [])

        if not jobs:
            print(f"No jobs returned for page {page}")
            continue

        all_jobs.extend(jobs)

    if not all_jobs:
        print("No jobs collected.")
        return pd.DataFrame()

    df = pd.json_normalize(all_jobs)

    df_clean = df[[
        "id",
        "title",
        "company.display_name",
        "location.display_name",
        "salary_min",
        "salary_max",
        "created",
        "category.label",
        "description"
    ]]

    # Add salary average
    df_clean["salary_avg"] = (
        df_clean["salary_min"].fillna(0) +
        df_clean["salary_max"].fillna(0)
    ) / 2

    # Convert created date
    df_clean["created"] = pd.to_datetime(df_clean["created"]).dt.date

    # Rename columns
    df_clean.columns = [
        "id",
        "title",
        "company",
        "location",
        "salary_min",
        "salary_max",
        "created",
        "category",
        "description",
        "salary_avg"
    ]

    return df_clean

if __name__ == "__main__":
    df = fetch_jobs()

    if not df.empty:
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

        raw_path = os.path.join("data", "raw", "jobs_raw.csv")
        processed_path = os.path.join("data", "processed", "jobs_clean.csv")

        df.to_csv(raw_path, index=False)
        df.to_csv(processed_path, index=False)

        print("Saved cleaned dataset with", len(df), "jobs.")
    else:
        print("No data saved.")
