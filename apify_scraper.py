from collections import deque

from apify_client import ApifyClient
from numpy.f2py.crackfortran import privatepattern


class JobScraper:
    def __init__(self, tokens):
        self.round_robin = deque(tokens)
    def get_next_token(self):
        token = self.round_robin.popleft()
        self.round_robin.append(token)
        return token


    def run_linkedin_job_scraper(self,token,company_job_url):
        """
        Run the LinkedIn job scraper on a specific company's job search URL.

        Args:
            company_job_url (str): Full LinkedIn job search URL for the company.
        Returns:
            list[dict]: List of job results with fields like job title, URL, etc.
            :param company_job_url:
            :param token:
        """
        client = ApifyClient(token)

        run_input = {
            "startUrls": [{"url": company_job_url}],
            "location": "Israel",
            "publishedAt": "r86400",
            "saveOnlyUniqueItems": False,
            "proxy": {"useApifyProxy": True}
        }
        print(f"📡 Running scraper on: {company_job_url}")
        run = client.actor("2rJKkhh7vjpX7pvjg").call(run_input=run_input)

        print("📥 Fetching results...")
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)

        print(f"✅ Retrieved {len(results)} job(s).")
        return results

    def try_all_tokens(self,search_url, company_name):
        for _ in range(len(self.round_robin)):
            token = self.get_next_token()
            try:
                print(f"🔑 Trying token for {company_name}...")
                return self.run_linkedin_job_scraper(token,search_url)
            except Exception as e:
                print(f"❌ Token failed: {e}")
        print(f"🚫 All tokens failed for {company_name}")
        return []

