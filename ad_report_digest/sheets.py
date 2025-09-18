from typing import List
from .models import MetricRecord
from .config import Settings, get_service_account_info


def write_to_sheet(settings: Settings, records: List[MetricRecord]):
    if not settings.spreadsheet_id:
        return  # no-op if not configured

    sa_info = get_service_account_info(settings)
    if not sa_info:
        return  # no-op if no credentials found

    # Lazy import Google libraries so the project can run without them in mock-only mode
    try:
        from google.oauth2.service_account import Credentials  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except Exception:
        return

    creds = Credentials.from_service_account_info(
        sa_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    # Disable discovery cache to avoid oauth2client file_cache warning
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)

    # Ensure the target tab exists before writing ranges like "{tab}!A1"
    _ensure_tab_exists(service, settings.spreadsheet_id, settings.tab_name)

    # Ensure header exists by reading current sheet size
    sheet = service.spreadsheets()
    header = [
        "date","platform","spend_usd","impressions","clicks","conversions","cpc","cpa","users","sessions","events"
    ]

    # Prepare values (sanitize NaN -> None for valid JSON)
    values = [
        _sanitize_row([
            r.date, r.platform, r.spend_usd, r.impressions, r.clicks, r.conversions,
            r.cpc, r.cpa, r.users, r.sessions, r.events
        ])
        for r in records
    ]

    # Append header if needed (best-effort: try to read first row)
    try:
        result = sheet.values().get(
            spreadsheetId=settings.spreadsheet_id,
            range=f"{settings.tab_name}!1:1"
        ).execute()
        current_header = result.get("values", [])
    except Exception:
        current_header = []

    if not current_header:
        sheet.values().update(
            spreadsheetId=settings.spreadsheet_id,
            range=f"{settings.tab_name}!A1",
            valueInputOption="RAW",
            body={"values": [header]},
        ).execute()
        start_row = 2
    else:
        start_row = 2

    # Append data at the end
    sheet.values().append(
        spreadsheetId=settings.spreadsheet_id,
        range=f"{settings.tab_name}!A{start_row}",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": values},
    ).execute()


def _sanitize_cell(v):
    # Convert NaN-like values to None; keep valid primitives as-is
    try:
        if v is None:
            return None
        # NaN doesn't equal itself
        if v != v:  # type: ignore
            return None
        return v
    except Exception:
        return v


def _sanitize_row(row):
    return [_sanitize_cell(v) for v in row]


def _ensure_tab_exists(service, spreadsheet_id: str, tab_name: str) -> None:
    """Create the tab if it doesn't exist."""
    try:
        meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        for sh in meta.get("sheets", []):
            props = sh.get("properties", {})
            if props.get("title") == tab_name:
                return
    except Exception:
        # If we can't read metadata, try creating the sheet anyway
        pass

    body = {
        "requests": [
            {"addSheet": {"properties": {"title": tab_name}}}
        ]
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body,
    ).execute()
