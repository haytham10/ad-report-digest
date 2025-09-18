from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import date


@dataclass
class MetricRecord:
    date: str  # ISO date string YYYY-MM-DD
    platform: str  # Google Ads | Meta Ads | GA4
    spend_usd: Optional[float] = None
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    conversions: Optional[float] = None
    cpc: Optional[float] = None
    cpa: Optional[float] = None
    users: Optional[int] = None
    sessions: Optional[int] = None
    events: Optional[int] = None

    def to_row(self) -> Dict[str, Any]:
        return asdict(self)
