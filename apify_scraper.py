from apify_client import ApifyClient



def run_linkedin_job_scraper(api_token, company_job_url):
    """
    Run the LinkedIn job scraper on a specific company's job search URL.

    Args:
        api_token (str): Your Apify API token.
        company_job_url (str): Full LinkedIn job search URL for the company.
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

