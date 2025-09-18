from datetime import date
from typing import Dict, Any


def fetch_ga4(target_date: date) -> Dict[str, Any]:
    # Mocked data
    return {
        "date": target_date.isoformat(),
        "platform": "GA4",
        "users": 1800,
        "sessions": 2400,
        "events": 5000,
    }
