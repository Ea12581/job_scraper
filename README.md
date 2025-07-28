# 🔍 LinkedIn Job Scraper

This Python project scrapes job listings from LinkedIn using the [Apify LinkedIn Job Scraper](https://apify.com/marketplace) actor, based on a list of company LinkedIn IDs. The results are filtered and written directly into a Google Sheet.
The scraper doing the search by this url struct:
https://www.linkedin.com/jobs/search/?f_C={company_id}&geoId={geo_id}

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
├── extract_companies_jobs.py                     # Entry point: controls full scraping and writing flow
├── apify_scraper.py           # Apify API client and token fallback logic
├── sheets_utils.py            # Google Sheets utilities (write, restart, filter jobs)
├── json_utils.py              # JSON file utilities (load, filter companies)
├── linkedin_utils.py          # LinkedIn-specific helpers (ID extraction, URL building)
├── companies_ids_example.JSON         # Input file with companies and their LinkedIn IDs
├── .env                       # Environment variables including Apify tokens
├── credentials.json           # Google Sheets service account credentials
```

---
## 🆕 Company ID Extractor (Google Sheets Integration)
This new module helps you extract LinkedIn company IDs automatically from a Google Sheet .xlsx file containing a "company" column.

⚙️ How It Works
The script:

Loads company names from an uploaded Google Sheet .xlsx (not a live sheet link).

Attempts multiple variants of each name to guess the correct LinkedIn profile URL.

Scrapes the LinkedIn company page using a stealthy headless browser.

Extracts the internal companyId for each matched company.

Saves results into companies_ids.JSON.

#📄 Example Google Sheet Input

| company          |
|------------------|
| OpenAI           |
| Microsoft        |
| CyberAISolutions |


#🧪 Running the Extractor
Add your .xlsx file and set the path in .env:

```env
COMPANIES_URL=companies_list.xlsx
```
Run:

```bash
python extract_companies_id.py
```
You’ll get updates in the console and companies_ids.JSON will be updated incrementally.

* another way is to use another scraper to get info on multiples companies by their url, but it needs another mini script to extract the data and make the companies_ids.JSON file
this scraper:
https://console.apify.com/actors/AjfNXEI9qTA2IdaAX/runs/5rlAeZ2Nc7WHb2yPf#output

---

## 🔐 Setup `.env`

Create a `.env` file in your project root with the following:

```env
APIFY_TOKEN=your_token_1
APIFY_TOKEN2=your_token_2
APIFY_TOKEN3=your_token_3
...
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
---

## 🔎 How to Find `companyId` (LinkedIn Internal ID)

Each company on LinkedIn has a unique internal ID (called `companyId`) used to construct job search URLs.

You can manually extract it using the steps below:

### ✅ Steps to Find `companyId`:

1. Go to the company's LinkedIn page.  
   Example: `https://www.linkedin.com/company/someCompany/`

2. Click on the jobs section

3. Roll down and click on the ***see all jobs** options.

4. Look on the url and search for:

```makefile
https://www.linkedin.com/jobs/search/?currentJobId=4261918251& ***f_C=12345***
```



5. The parameter f_C = `12345` is the internal LinkedIn `companyId`.

### 📄 Example `companies_ids.JSON` Entry

```json
[
{
 "companyName": "AwosomeCompany",
 "companyId": 1234567
},
{
 "companyName": "CyberAISolutions",
 "companyId": 9876543
}
]
```

---

## 🚀 Running the Scraper

Run the following command:

```bash
python extract_companies_jobs.py
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
