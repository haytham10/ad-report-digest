from datetime import date
from typing import Dict, Any


def fetch_meta_ads(target_date: date) -> Dict[str, Any]:
    # Mocked data
    return {
        "date": target_date.isoformat(),
        "platform": "Meta Ads",
        "spend_usd": 2100.0,
        "impressions": 65000,
        "clicks": 650,
        "conversions": 171,
        "cpc": 2100.0 / 650 if 650 else None,
        "cpa": 2100.0 / 171 if 171 else None,
    }
