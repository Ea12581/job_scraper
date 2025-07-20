import json
from apify_scraper import JobScraper
from json_utils import load_company_data
from linkedin_utils import build_linkedin_jobs_url
from sheets_utils import write_jobs_to_google_sheet, restart_file, filter_job_attributes
from dotenv import load_dotenv
from collections import deque
import os
load_dotenv()


API_TOKEN_1 = os.getenv("APIFY_TOKEN_1")
API_TOKEN_2 = os.getenv("APIFY_TOKEN_2")
API_TOKEN_3 = os.getenv("APIFY_TOKEN_3")
API_TOKEN_4 = os.getenv("APIFY_TOKEN_4")
API_TOKEN_5 = os.getenv("APIFY_TOKEN_5")
TOKENS = (token for token in [API_TOKEN_1, API_TOKEN_2,API_TOKEN_3,API_TOKEN_4,API_TOKEN_5] if token)
MAX_JOBS=50000
COMPANIES_DATA_PATH = "companies_ids.JSON"
ALLOWED_JOB_KEYS = [
    "companyName",
    "jobTitle",
    "jobUrl",
    "publishedAt",
    "postedTime",
    "jobDescription",
    "sector",
    "appliesCount",
    "applyUrl",
    "experienceLevel",
    "workplaceTypes",
    "posterFullName",
    "posterProfileUrl",
]

SHEET_ID=os.getenv("SHEET_ID")


def main():
    companies = load_company_data(COMPANIES_DATA_PATH)
    with restart_file(SHEET_ID):
        print("✅ Google Sheet cleared.")

    total_jobs = 0
    scraper = JobScraper(TOKENS)
    for company in companies[:1]:
        if total_jobs >= MAX_JOBS:
            break
        name = company.get("name") or company.get("companyName")
        company_id = company.get("companyId")

        if not name or not company_id:
            print(f"⚠️ Missing name or ID for company: {company}")
            continue

        print(f"🔍 Scraping jobs for {name} (ID: {company_id})")
        search_url = build_linkedin_jobs_url(company_id)

        try:
            jobs = scraper.try_all_tokens(search_url,company_name=name)
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
