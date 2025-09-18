from typing import List, Dict, Any
import pandas as pd
from .models import MetricRecord


STANDARD_FIELDS = [
    "date",
    "platform",
    "spend_usd",
    "impressions",
    "clicks",
    "conversions",
    "cpc",
    "cpa",
    "users",
    "sessions",
    "events",
]


def normalize_records(records: List[Dict[str, Any]]) -> List[MetricRecord]:
    # Use pandas to coerce and fill missing fields uniformly
    df = pd.DataFrame(records)
    for col in STANDARD_FIELDS:
        if col not in df.columns:
            df[col] = None
    df = df[STANDARD_FIELDS]

    # Replace NaN/NaT with None for JSON compatibility downstream
    df = df.where(pd.notnull(df), None)

    # Ensure types where possible
    df["date"] = df["date"].astype(str)
    df["platform"] = df["platform"].astype(str)

    out: List[MetricRecord] = []
    for _, row in df.iterrows():
        out.append(MetricRecord(**row.to_dict()))
    return out


def build_digest_text(records: List[MetricRecord], digest_date: str) -> str:
    # Create human-readable digest
    lines = [f"📊 Daily Ad Digest – {digest_date}"]
    by_platform = {r.platform: r for r in records}

    if "Google Ads" in by_platform:
        r = by_platform["Google Ads"]
        lines.append(
            f"Google Ads: ${r.spend_usd:,.0f} spend | {int(r.clicks or 0)} clicks | CPA ${((r.cpa or 0)):.1f}"
        )
    if "Meta Ads" in by_platform:
        r = by_platform["Meta Ads"]
        lines.append(
            f"Meta Ads: ${r.spend_usd:,.0f} spend | {int(r.clicks or 0)} clicks | CPA ${((r.cpa or 0)):.1f}"
        )
    if "GA4" in by_platform:
        r = by_platform["GA4"]
        lines.append(
            f"GA4: {int(r.users or 0)} users, {int(r.sessions or 0)} sessions"
        )

    return "\n".join(lines)
