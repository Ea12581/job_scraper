
import json

def load_company_data(json_path: str):
    """
    Load JSON and return list of (company_name, company_id)
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    company_info = []
    for company in data:
        name = company.get("companyName") or company.get("name")
        company_id = company.get("companyId")
        if name and company_id:
            company_info.append({
                "company_name": name,
                "company_id": company_id
            })

    return company_info

def extract_basic_company_info(input_path: str, output_path: str):
    """
    Extracts only 'companyName' and 'companyId' from a JSON file and saves to a new JSON file.

    Args:
        input_path (str): Path to the input JSON file containing full company data.
        output_path (str): Path where the simplified JSON file will be saved.
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        companies = json.load(infile)

    simplified = []
    for company in companies:
        name = company.get("companyName") or company.get("name")
        company_id = company.get("companyId")
        if name and company_id:
            simplified.append({
                "companyName": name,
                "companyId": company_id
            })

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(simplified, outfile, ensure_ascii=False, indent=2)

    print(f"✅ Extracted {len(simplified)} companies to {output_path}")
