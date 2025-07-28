import pytest
from unittest.mock import patch, MagicMock
from linkedin_utils import get_company_id_safe


@pytest.fixture
def mock_fetcher_success():
    with patch("company_id_fetcher.LinkedInCompanyIDFetcher") as mock_class:
        mock_instance = MagicMock()
        mock_instance.get_company_info.return_value = ("123456", "cyberark")
        mock_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_fetcher_failure():
    with patch("company_id_fetcher.LinkedInCompanyIDFetcher") as mock_class:
        mock_instance = MagicMock()
        mock_instance.get_company_id.return_value = None
        mock_class.return_value = mock_instance
        yield mock_instance





def test_get_company_id_safe_failure(mock_fetcher_failure):
    result = get_company_id_safe("NonExistent Company")
    assert result is None