import argparse
from datetime import datetime, date
from typing import List

from .config import Settings
from .fetchers.google_ads import fetch_google_ads
from .fetchers.meta_ads import fetch_meta_ads
from .fetchers.ga4 import fetch_ga4
from .aggregator import normalize_records, build_digest_text
from .sheets import write_to_sheet
from .slack_digest import send_slack_digest
from .utils.logging_setup import setup_logging, csv_log


def run_pipeline(run_date: date):
    logger = setup_logging()
    settings = Settings()

    try:
        # Fetch
        records_raw: List[dict] = []
        records_raw.append(fetch_google_ads(run_date))
        records_raw.append(fetch_meta_ads(run_date))
        records_raw.append(fetch_ga4(run_date))

        # Normalize
        records = normalize_records(records_raw)

        # Sheets
        write_to_sheet(settings, records)

        # Slack
        digest_text = build_digest_text(records, run_date.isoformat())
        sent = send_slack_digest(settings.slack_webhook_url, digest_text)

        logger.info("Run success | sent_slack=%s", sent)
        csv_log("success", f"sent_slack={sent}")
    except Exception as e:
        logger.exception("Run failed: %s", e)
        csv_log("error", str(e))
        raise


def parse_args():
    p = argparse.ArgumentParser(description="Daily ad report digest")
    p.add_argument("--date", default="today", help="ISO date YYYY-MM-DD or 'today'")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.date == "today":
        d = datetime.utcnow().date()
    else:
        d = datetime.fromisoformat(args.date).date()
    run_pipeline(d)
