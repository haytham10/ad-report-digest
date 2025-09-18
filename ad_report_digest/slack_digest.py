from typing import Optional
import requests # type: ignore


def send_slack_digest(webhook_url: Optional[str], text: str) -> bool:
    if not webhook_url:
        return False
    try:
        resp = requests.post(webhook_url, json={"text": text}, timeout=10)
        return 200 <= resp.status_code < 300
    except Exception:
        return False
