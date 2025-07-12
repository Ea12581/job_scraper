# job_scraper/apify_scraper.py
import json

from apify_client import ApifyClient



def run_linkedin_job_scraper(api_token, company_job_url, keywords=None, location=None, published_at="r604800"):
    """
    Run the LinkedIn job scraper on a specific company's job search URL.

    Args:
        api_token (str): Your Apify API token.
        company_job_url (str): Full LinkedIn job search URL for the company.
        keywords (list[str]): Optional list of keywords to filter by.
        location (str): Optional location string.
        published_at (str): Time range, e.g., "r86400" for past 24h or "r604800" for past 7 days.

    Returns:
        list[dict]: List of job results with fields like job title, URL, etc.
    """
    client = ApifyClient(api_token)

    run_input = {
        "startUrls": [{"url": company_job_url}],
        "location": "Israel",
        "publishedAt": "r86400",
        "saveOnlyUniqueItems": False,
        "proxy": { "useApifyProxy": True }
    }
    print("Sending to Apify:\n", json.dumps(run_input, indent=2))
    print(f"📡 Running scraper on: {company_job_url}")
    run = client.actor("2rJKkhh7vjpX7pvjg").call(run_input=run_input)

    print("📥 Fetching results...")
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    print(f"✅ Retrieved {len(results)} job(s).")
    return results

def try_all_tokens(search_url, company_name,tokens):
    for token in tokens:
        try:
            print(f"🔑 Trying token for {company_name}...")
            return run_linkedin_job_scraper(token, search_url)
        except Exception as e:
            print(f"❌ Token failed: {e}")
    print(f"🚫 All tokens failed for {company_name}")
    return []

