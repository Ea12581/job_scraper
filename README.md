# 🔍 LinkedIn Job Scraper

This Python project scrapes job listings from LinkedIn using the [Apify LinkedIn Job Scraper](https://apify.com/marketplace) actor, based on a list of company LinkedIn IDs. The results are filtered and written directly into a Google Sheet.

---

## 📌 Features

- ✅ Reads companies from a local JSON file (`companies_ids.JSON`)
- ✅ Dynamically builds LinkedIn job search URLs using internal company IDs
- ✅ Uses multiple Apify tokens with failover handling (token rotation)
- ✅ Extracts and filters relevant job attributes (e.g., title, URL, posting date, etc.)
- ✅ Appends job listings to a specified Google Sheet
- ✅ Supports Google Sheets integration via `gspread` and `pandas`

---

## 📁 Project Structure

```bash
.
├── main.py                     # Entry point: controls full scraping and writing flow
├── apify_scraper.py           # Apify API client and token fallback logic
├── sheets_utils.py            # Google Sheets utilities (write, restart, filter jobs)
├── json_utils.py              # JSON file utilities (load, filter companies)
├── linkedin_utils.py          # LinkedIn-specific helpers (ID extraction, URL building)
├── companies_ids.JSON         # Input file with companies and their LinkedIn IDs
├── .env                       # Environment variables including Apify tokens
├── credentials.json           # Google Sheets service account credentials

🔐 Setup .env
Create a .env file with:

env
Copy
Edit
APIFY_TOKEN=your_token_1
APIFY_TOKEN2=your_token_2
APIFY_TOKEN3=your_token_3
Only valid tokens are used in a fallback mechanism if limits are reached. You can create tokens inside the API section in [Apify LinkedIn Job Scraper](https://apify.com/marketplace) 

🔑 Google Sheets Credentials
Download your Google service account key as credentials.json and share the Google Sheet with the associated email.

Set correct scopes inside sheets_utils.py:

python
Copy
Edit
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

🚀 Running the Scraper
bash
Copy
Edit
python main.py

This will:

Load companies from companies_ids.JSON

Scrape LinkedIn for job listings

Filter job attributes

Append them to your configured Google Sheet

🧠 Example of Saved Fields
The scraper saves these job attributes:

companyName

jobTitle

jobUrl

publishedAt

postedTime

sector

applyUrl

appliesCount

experienceLevel

workplaceTypes

posterFullName

posterProfileUrl

📈 Google Sheet Output
The job listings will be written into the sheet specified by SHEET_ID in main.py, with column headers automatically inserted.


🙌 Acknowledgments
Apify LinkedIn Job Scraper

gspread

pandas

vbnet
Copy
Edit
 
