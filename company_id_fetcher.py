from typing import Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time
import re

class LinkedInCompanyIDFetcher:
    def __init__(self):
        self.driver = self._init_browser()

    def _init_browser(self):
        """initialize a headless browser."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 ...")
        return webdriver.Chrome(options=options)

    def get_company_info(self, company_name: str) -> Tuple[str,str,str] | None:
        """extract the internal LinkedIn company ID from a company name."""
        try:
            profile_url = self._get_linkedin_profile(company_name)
            if not profile_url:
                return None

            html = self._fetch_profile_html(profile_url)
            company_id = self._extract_company_id(html)
            company_linkdin_name = self._extract_company_name(html)
            return company_id, company_linkdin_name,profile_url

        finally:
            self.driver.quit()
    def get_company_id_by_url(self,company_url: str ) -> Tuple[str,str]:
        html = self._fetch_profile_html(company_url)
        company_id = self._extract_company_id(html)
        company_linkdin_name = self._extract_company_name(html)
        return company_id, company_linkdin_name

    def _get_linkedin_profile(self, company_name: str) -> str:
        return f"https://www.linkedin.com/company/{quote(company_name.strip().lower())}/"

    def _fetch_profile_html(self, profile_url: str) -> str:
        self.driver.get(profile_url)
        time.sleep(2)
        return self.driver.page_source

    def _extract_company_id(self, html: str) -> str | None:
        # look for the LinkedIn internal ID (organization ID)
        patterns = [
            r'"objectUrn":"urn:li:organization:(\d+)"',
            r'"entityUrn":"urn:li:organization:(\d+)"',
            r'urn:li:organization:(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)

        return None



    def _extract_company_name(self,html_content):
        """
        Extracts the company name from LinkedIn company profile HTML.

        Args:
            html_content (str): The full HTML content of the LinkedIn company profile page.

        Returns:
            str: The extracted company name, or None if not found.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # look for a specific H1 with a characteristic class ---
        company_name_h1 = soup.find('h1', class_='top-card-layout__title')
        if company_name_h1:
            return company_name_h1.get_text(strip=True)

        # look for title within a specific div/section ---

        company_name_div = soup.find('div', class_='org-top-card-summary__title-and-actions')
        if company_name_div:
            company_name_h1_in_div = company_name_div.find('h1', class_='org-top-card-summary__title')
            if company_name_h1_in_div:
                return company_name_h1_in_div.get_text(strip=True)

        # look at the <title> tag
        # The page <title> usually contains the company name
        # Example: "Company Name | LinkedIn"
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # Use regex to extract the part before "| LinkedIn"
            match = re.match(r'^(.*?)\s*\|\s*LinkedIn$', title_text)
            if match:
                return match.group(1).strip()

        # look for meta tags (less common for the primary name, but good for validation) ---
        # <meta property="og:title" content="Company Name | LinkedIn" />
        og_title_meta = soup.find('meta', property='og:title')
        if og_title_meta:
            content = og_title_meta.get('content', '')
            match = re.match(r'^(.*?)\s*\|\s*LinkedIn$', content)
            if match:
                return match.group(1).strip()

