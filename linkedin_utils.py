import time
from typing import List

from company_id_fetcher import LinkedInCompanyIDFetcher
from json_utils import load_existing_companies, save_companies, COMPANIES_FILE
from difflib import SequenceMatcher


RETRY_LIMIT = 2
SLEEP_BETWEEN = 2

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def build_linkedin_jobs_url(company_id: int, geo_id: int = 101620260) -> str:
    """
    construct LinkedIn job search URL for a company using its internal ID.

    Args:
        company_id (int): LinkedIn internal company ID.
        geo_id (int): LinkedIn geoId for location (default is Israel: 101620260)

    Returns:
        str: Constructed LinkedIn jobs URL.
    """
    return (
        f"https://www.linkedin.com/jobs/search/?f_C={company_id}&geoId={geo_id}"
    )


def get_company_id_safe(company_name: str) -> int | None:
    """
    attempt to find a LinkedIn company ID using name variations.
    tries:
    - original (with hyphens if any)
    - all lowercase joined by hyphens
    - all lowercase joined without spaces
    - progressive truncation of name
    """
    import time
    import re

    name_parts = re.findall(r"\w+", company_name.lower())

    attempts = set()
    attempts.add("-".join(name_parts))
    attempts.add("".join(name_parts))

    for i in range(len(name_parts) - 1, 0, -1):
        truncated = name_parts[:i]
        attempts.add("-".join(truncated))
        attempts.add("".join(truncated))

    for name_variant in attempts:
        for attempt_num in range(1, RETRY_LIMIT + 1):
            try:
                print(f"[LOOKUP] ({attempt_num}/{RETRY_LIMIT}) Trying: {name_variant}")
                fetcher = LinkedInCompanyIDFetcher()
                company_id, company_linkdin_name, url = fetcher.get_company_info(name_variant)
                if company_id and company_linkdin_name.lower() == company_name.lower():
                    print(f"[✅ MATCH] {company_name} → {name_variant} → {company_id}")
                    print(f"url: {url}")
                    return int(company_id)
            except Exception as e:
                print(f"[ERROR] {name_variant} → {e}")
                time.sleep(1)

    print(f"[❌ FAILED] No match for {company_name} after trying {len(attempts)} variations.")
    return None


def generate_company_ids(companies: List[str]):
    existing = load_existing_companies()
    updated = existing.copy()
    for company in companies:
        if company in updated:
            print(f"[SKIP] {company} already scraped")
            continue

        company_id = get_company_id_safe(company)
        if company_id:
            updated[company] = company_id
            print(f"[✅] {company} → {company_id}")
        else:
            print(f"[❌] Failed to find ID for {company}")
        save_companies(updated)
        time.sleep(SLEEP_BETWEEN)

    print(f"[✔️ DONE] Saved {len(updated)} companies to {COMPANIES_FILE}")