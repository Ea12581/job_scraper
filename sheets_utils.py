from typing import List
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from contextlib import contextmanager
from datetime import datetime



def filter_job_attributes(job: dict, allowed_keys: list) -> dict:
    """
    Filters a job dictionary to include only the allowed keys.

    Args:
        job (dict): The original job dictionary.
        allowed_keys (list): List of keys to keep.

    Returns:
        dict: A new dictionary with only the whitelisted keys.
    """
    cleaned_job = {}
    for key in allowed_keys:
        if key in job:
            value = job[key]
            # Clean up unwanted link text or misjoined fields
            if isinstance(value, str):
                # Remove URLs accidentally joined with text
                value = value.strip()
                if "http" in value and not value.startswith("http"):
                    parts = value.split("http")
                    value = parts[0].strip()
            cleaned_job[key] = value
    date_str = cleaned_job["publishedAt"]
    parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    cleaned_job["publishedAt"] = str(parsed_date)
    return cleaned_job

@contextmanager
def restart_file(sheet_url: str):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

    # Connect to Google Sheets
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.sheet1
    worksheet.clear()
    yield worksheet


def write_jobs_to_google_sheet(sheet_url: str, jobs_data: List[dict]):
    """
    Writes job data to a Google Sheet using pandas.
    Args:
        sheet_url (str): URL of the Google Sheet.
        jobs_data (List[dict]): List of job dictionaries containing keys: 'company', 'title', 'link', 'postedAt'.
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.sheet1

    df = pd.DataFrame(jobs_data)
    is_empty = not worksheet.acell('A1').value
    next_row = len(worksheet.get_all_values()) + 1 if not is_empty else 1

    if is_empty:
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    else:
        worksheet.update(f'A{next_row}', df.values.tolist())

