
import json
import os

COMPANIES_FILE = "companies_ids_example.JSON"

def load_company_data(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    company_info = []
    for company in data:
        name = company.get("companyName") or company.get("name")
        company_id = company.get("companyId")
        if name and company_id:
            company_info.append({
                "companyName": name,
                "companyId": company_id
            })

    return company_info

def load_existing_companies() -> dict:
    """Load existing company ID mappings if file exists, otherwise return empty dict."""
    if os.path.exists(COMPANIES_FILE):
        with open(COMPANIES_FILE, "r", encoding="utf-8") as f:
            try:
                return {entry["companyName"]: entry["companyId"] for entry in json.load(f)}
            except json.JSONDecodeError:
                return {}
    return {}

def save_companies(company_dict: dict):
    """Save dictionary to JSON file in the requested structure and order."""
    sorted_companies = sorted(company_dict.items())  # Alphabetical by company name
    structured = [
        {
            "companyName": name,
            "companyId": company_id
        } for name, company_id in sorted_companies
    ]
    with open(COMPANIES_FILE, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

