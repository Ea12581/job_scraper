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
```

---

## 🔐 Setup `.env`

Create a `.env` file in your project root with the following:

```env
APIFY_TOKEN=your_token_1
APIFY_TOKEN2=your_token_2
APIFY_TOKEN3=your_token_3
```

These tokens are used in fallback order if any reach their usage limits.  
Generate your tokens from the [Apify Console](https://console.apify.com/account/integrations?tab=api-clients).

---

## 🔑 Google Sheets Credentials

1. Create a [Google Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Download the `credentials.json` file to your project.
3. Share the target Google Sheet with the service account email.
4. Make sure `sheets_utils.py` includes the proper scope:

```python
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
```

---

## 🚀 Running the Scraper

Run the following command:

```bash
python main.py
```

This script will:

- Load companies from `companies_ids.JSON`
- Scrape LinkedIn jobs via Apify
- Filter only allowed job fields
- Write jobs to the configured Google Sheet

---

## 🧠 Job Attributes Saved

The following fields are saved per job:

- `companyName`
- `jobTitle`
- `jobUrl`
- `publishedAt`
- `postedTime`
- `sector`
- `applyUrl`
- `appliesCount`
- `experienceLevel`
- `workplaceTypes`
- `posterFullName`
- `posterProfileUrl`

---

## 📈 Google Sheet Output

Job data is written to the Google Sheet defined in `SHEET_ID` (inside `main.py`).  
Headers are inserted once, and new jobs are appended below.

---

## 🙌 Built With

- [Apify LinkedIn Job Scraper](https://apify.com/marketplace)
- [gspread](https://github.com/burnash/gspread)
- [pandas](https://pandas.pydata.org/)
