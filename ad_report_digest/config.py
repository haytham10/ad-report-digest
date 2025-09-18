import json
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv # type: ignore


load_dotenv()


@dataclass
class Settings:
    use_mock: bool = os.getenv("USE_MOCK", "1") == "1"
    timezone: str = os.getenv("TIMEZONE", "UTC")

    # Google Sheets
    spreadsheet_id: Optional[str] = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
    tab_name: str = os.getenv("GOOGLE_SHEETS_TAB_NAME", "DailyMetrics")

    # Google Service Account
    sa_json_inline: Optional[str] = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sa_json_file: Optional[str] = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

    # Slack
    slack_webhook_url: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")


def get_service_account_info(settings: Settings):
    if settings.sa_json_inline:
        return json.loads(settings.sa_json_inline)
    if settings.sa_json_file and os.path.exists(settings.sa_json_file):
        with open(settings.sa_json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
