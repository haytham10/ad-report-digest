from datetime import date
from typing import Dict, Any


def fetch_google_ads(target_date: date) -> Dict[str, Any]:
    # Mocked data
    return {
        "date": target_date.isoformat(),
        "platform": "Google Ads",
        "spend_usd": 3200.0,
        "impressions": 50000,
        "clicks": 500,
        "conversions": 201,
        "cpc": 3200.0 / 500 if 500 else None,
        "cpa": 3200.0 / 201 if 201 else None,
    }
