
from linkedin_utils import generate_company_ids
from sheets_utils import extract_company_names_from_google_sheet_xlsx
from dotenv import load_dotenv
import os
load_dotenv()




companies_url = os.getenv("COMPANIES_URL")
company_names = extract_company_names_from_google_sheet_xlsx(companies_url)
generate_company_ids(company_names)
