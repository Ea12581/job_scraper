import json
from apify_scraper import try_all_tokens
from sheets_utils import write_jobs_to_google_sheet, restart_file, filter_job_attributes
from dotenv import load_dotenv
import os
load_dotenv()


API_TOKEN_1 = os.getenv("APIFY_TOKEN")
API_TOKEN_2 = os.getenv("APIFY_TOKEN2")
API_TOKEN_3 = os.getenv("APIFY_TOKEN3")
TOKENS = [token for token in [API_TOKEN_1, API_TOKEN_2,API_TOKEN_3] if token]
MAX_JOBS=50000
COMPANIES_DATA_PATH = "companies_ids.JSON"
ALLOWED_JOB_KEYS = [
    "companyName",
    "jobTitle",
    "jobUrl",
    "publishedAt",
    "postedTime",
    "sector",
    "applyUrl",
    "appliesCount",
    "experienceLevel",
    "workplaceTypes",
    "posterFullName",
    "posterProfileUrl",
]

SHEET_ID=os.getenv("SHEET_ID")
def load_companies(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_search_url(company_id):
    return f"https://www.linkedin.com/jobs/search/?f_C={company_id}&geoId=101620260"

def main():
    companies = load_companies(COMPANIES_DATA_PATH)
    with restart_file(SHEET_ID):
        print("✅ Google Sheet cleared.")

    total_jobs = 0

    for company in companies:
        if total_jobs >= MAX_JOBS:
            break
        name = company.get("name") or company.get("companyName")
        company_id = company.get("companyId")

        if not name or not company_id:
            print(f"⚠️ Missing name or ID for company: {company}")
            continue

        print(f"🔍 Scraping jobs for {name} (ID: {company_id})")
        search_url = build_search_url(company_id)

        try:
            jobs = try_all_tokens(search_url, name,TOKENS)
            if not jobs:
                continue
        except Exception as e:
            print(f"❌ Failed to scrape {name}: {e}")
            continue

        filtered_jobs = []
        for job in jobs:
            job["companyName"] = name
            filtered_jobs.append(filter_job_attributes(job, ALLOWED_JOB_KEYS))

        if jobs:
            print(f"{len(jobs)} jobs in {name}.")
        else:
            print(f"⚠️ No job results found on {name}.")

        if filtered_jobs:
            try:
                write_jobs_to_google_sheet(SHEET_ID, filtered_jobs)
                total_jobs += len(filtered_jobs)
                print(f"✅ Added {len(filtered_jobs)} jobs for {name} (Total: {total_jobs})")
            except Exception as e:
                print(f"❌ Error writing jobs for {name}: {e}")
        else:
            print(f"⚠️ No jobs found for {name}")


if __name__ == "__main__":
    main()
