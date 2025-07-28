import os
import sys

import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from company_id_fetcher import LinkedInCompanyIDFetcher

# Sample HTML with both title and objectUrn
sample_html_full = """
<html>
<head>
    <title>Checkmarx | LinkedIn</title>
    <meta property="og:title" content="Checkmarx">
</head>
<body>
    <code>{"objectUrn":"urn:li:organization:223472"}</code>
</body>
</html>
"""

# HTML with only og:title
sample_html_og_only = """
<head>
    <meta property="og:title" content="Cyberark">
</head>
"""

# HTML with only fallback urn
sample_html_urn_fallback = """
<body>
    Some data... urn:li:organization:999999
</body>
"""

# HTML with no matches
sample_html_invalid = """
<head>
    <title>Not LinkedIn</title>
</head>
"""

@pytest.fixture
def fetcher():
    return LinkedInCompanyIDFetcher()

def test_extract_company_id_from_full_html(fetcher):
    assert fetcher._extract_company_id(sample_html_full) == "223472"

def test_extract_company_id_from_fallback(fetcher):
    assert fetcher._extract_company_id(sample_html_urn_fallback) == "999999"

def test_extract_company_id_none(fetcher):
    assert fetcher._extract_company_id(sample_html_invalid) is None

def test_extract_name_from_title(fetcher):
    assert fetcher._extract_company_name(sample_html_full) == "Checkmarx"

def test_extract_name_from_og(fetcher):
    assert fetcher._extract_company_name(sample_html_og_only) == "Cyberark"

def test_extract_name_none(fetcher):
    assert fetcher._extract_company_name(sample_html_invalid) is None

def test_get_company_info_with_mock(monkeypatch):
    fetcher = LinkedInCompanyIDFetcher()

    # Patch the browser-dependent parts
    fetcher._get_linkedin_profile = lambda name: "mocked-url"
    fetcher._fetch_profile_html = lambda url: sample_html_full

    result = fetcher.get_company_info("checkmarx")
    assert result == ("223472", "Checkmarx")
