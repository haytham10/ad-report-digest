# Ad Report Digest (Demo Workflow)

Automate daily ad performance reporting across Google Ads, Meta Ads, and GA4. The pipeline normalizes metrics, writes them to Google Sheets, and posts a Slack digest at 06:00 UTC. Includes a mock mode so you can demo end‑to‑end without API access.

## Overview
- Daily schedule (06:00 UTC) or manual run
- Fetch platform metrics (mock by default)
- Normalize to a common schema
- Append to Google Sheets (service account)
- Post Slack digest (incoming webhook)
- Log success/errors to file and CSV

## Architecture
- Fetchers: `ad_report_digest/fetchers/*.py`
- Normalization & digest: `ad_report_digest/aggregator.py`
- Sheets writer: `ad_report_digest/sheets.py`
- Slack: `ad_report_digest/slack_digest.py`
- Config: `ad_report_digest/config.py`
- Entrypoint: `ad_report_digest/main.py`

## Project structure
```
ad_report_digest/
  fetchers/
    google_ads.py
    meta_ads.py
    ga4.py
  utils/
    logging_setup.py
  aggregator.py
  sheets.py
  slack_digest.py
  config.py
  main.py
data/mock/
.github/workflows/daily-digest.yml
```

## Setup
1) Requirements: Python 3.10+
2) Install dependencies
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```
3) Configure environment
- Copy `.env.example` to `.env`
- Set at least:
  - `USE_MOCK=1` (keeps data mocked; set to 0 when you add real API fetchers)
  - `GOOGLE_SHEETS_SPREADSHEET_ID` to enable Sheets writes
  - One of `GOOGLE_SERVICE_ACCOUNT_JSON` (inline JSON) or `GOOGLE_SERVICE_ACCOUNT_FILE` (path)
  - `SLACK_WEBHOOK_URL` to post digests

## Quickstart (mock data)
```bash
python -m ad_report_digest.main --date today
```
Outputs
- Sheet: creates the tab (default `DailyMetrics`) if missing, writes header if missing, and appends rows
- Slack: posts a digest if `SLACK_WEBHOOK_URL` is set
- Logs: `logs/run.log` and `logs/run_log.csv`

## Configuration
Environment variables (see `.env.example`):
- `USE_MOCK` — use mock data (1/0)
- `TIMEZONE` — informational label; scheduling uses UTC in GitHub Actions
- `GOOGLE_SHEETS_SPREADSHEET_ID` — target spreadsheet ID
- `GOOGLE_SHEETS_TAB_NAME` — tab to write to (default `DailyMetrics`)
- `GOOGLE_SERVICE_ACCOUNT_JSON` — inline JSON string for service account credentials
- `GOOGLE_SERVICE_ACCOUNT_FILE` — path to JSON credentials file
- `SLACK_WEBHOOK_URL` — Slack incoming webhook URL

## Google Sheets setup
1. Create a spreadsheet and copy its ID
2. Share it with your service account email (from the JSON)
3. Set the env vars above

Behavior
- Auto-creates the tab if it does not exist
- Writes headers when missing
- Replaces NaN with empty cells before sending to Sheets
- Google client libraries are imported lazily (project runs in pure mock mode without them)

## Slack setup
1. Create an Incoming Webhook in Slack and copy the URL
2. Set `SLACK_WEBHOOK_URL`
3. Run the pipeline; a digest similar to below will post:

Example digest
📊 Daily Ad Digest – 2025-02-10
Google Ads: $3,200 spend | 500 clicks | CPA $15.9
Meta Ads: $2,100 spend | 650 clicks | CPA $12.3
GA4: 1,800 users, 2,400 sessions

## Scheduling (GitHub Actions)
Workflow: `.github/workflows/daily-digest.yml`
- Runs daily at 06:00 UTC and supports manual dispatch
- Recommended repository secrets:
  - `SLACK_WEBHOOK_URL`
  - `GOOGLE_SERVICE_ACCOUNT_JSON`
  - `GOOGLE_SHEETS_SPREADSHEET_ID`

## Troubleshooting
- Sheets: “Unable to parse range” — ensure the service account has access; the app will create the tab if permitted
- Sheets: “Invalid JSON payload” — indicates NaN/Infinity; the writer sanitizes values, but confirm your fetchers return valid numbers
- Slack: Not posting — verify `SLACK_WEBHOOK_URL` and that Slack workspace allows incoming webhooks
- Import errors in mock mode — OK; Google libraries are lazy-imported and skipped when missing

## Development
- Run for a specific date:
  ```bash
  python -m ad_report_digest.main --date 2025-09-17
  ```
- Logs are stored in `logs/`
- Keep secrets out of source control; use `.env` locally and GitHub Secrets in CI

## Next steps
- Implement real API calls in `fetchers/` and set `USE_MOCK=0`
- Optional: append run status to a "Log" tab in Sheets
- Add unit tests for normalization and digest formatting

## License
MIT
