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
