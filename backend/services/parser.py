"""Extracts task rows from an email body.

Pure function, no I/O - takes a raw email body and returns structured task
rows so it can be unit tested against sample email bodies without a live
mailbox or database.

Table format (HTML vs. plain text) is not yet confirmed (see CLAUDE.md
"Open decisions"). Swap the body of parse_task_rows() once real sample
emails are available; the ParsedTaskRow contract below should not need to
change.
"""

from datetime import datetime
from io import BytesIO

import openpyxl

from models.task import ParsedTaskRow


def parse_task_rows(email_body: str, content_type: str = "html") -> list[ParsedTaskRow]:
    """Parse the task table inside an email body into one or more rows.

    Args:
        email_body: raw HTML or plain-text body of the email.
        content_type: "html" or "text", as reported by the mail client.

    Returns:
        One ParsedTaskRow per task found in the body's table. An email with
        no recognizable table returns an empty list rather than raising.
    """
    if content_type == "html":
        return _parse_html_table(email_body)
    return _parse_plain_text_table(email_body)


def _parse_html_table(email_body: str) -> list[ParsedTaskRow]:
    raise NotImplementedError(
        "HTML table parsing not yet implemented - needs sample emails to confirm structure"
    )


def _parse_plain_text_table(email_body: str) -> list[ParsedTaskRow]:
    raise NotImplementedError(
        "Plain-text table parsing not yet implemented - needs sample emails to confirm structure"
    )


# Exact header -> real `tasks` column mapping, confirmed against a live
# sample export ("HGBU Supplier Schedule ... .xlsx") and the actual Supabase
# schema (checked via `select *` - see conversation, not guessed). Not
# fuzzy/alias matching on purpose: these are precise business columns, and a
# silent near-match would corrupt data rather than fail loudly.
_EXCEL_HEADER_TO_COLUMN = {
    "supplier name": "supplier_name",
    "resource": "resource",
    "resource start date / time": "resource_start",
    "resource end date / time": "resource_end",
    "hours allocated": "hours_allocated",
    "project #": "project_number",
    "project name": "project_name",
    "task number": "task_number",
    "pm": "pm",
    "resource manager": "resource_manager",
    "project status": "project_status",
    "project country": "project_country",
    "remote / on-site": "remote_onsite",
    "brand": "brand",
    "po": "po",
    "sow": "sow",
    "rate type": "rate_type",
}

# The primary key of `tasks` (project_name, project_number, task_number) -
# every row must have all three or it can't be upserted.
_REQUIRED_COLUMNS = {"project_name", "project_number", "task_number"}


def parse_excel_to_task_rows(content: bytes) -> list[dict]:
    """Parse an .xlsx attachment into raw dicts matching the real `tasks`
    table columns (see _EXCEL_HEADER_TO_COLUMN).

    Unlike parse_task_rows() this is not a ParsedTaskRow - the `tasks` table
    has no title/description columns, so there's no shared contract to
    validate against; callers get plain dicts ready for
    task_repository.upsert_task(). A row missing any of the 3 primary-key
    columns is skipped rather than raising, since a trailing blank row is
    common in exported spreadsheets.
    """
    workbook = openpyxl.load_workbook(BytesIO(content), data_only=True)
    sheet = workbook.active

    rows_iter = sheet.iter_rows(values_only=True)
    header = next(rows_iter, None)
    if header is None:
        return []

    column_by_index = {}
    for index, cell in enumerate(header):
        header_text = str(cell).strip().lower() if cell is not None else ""
        if header_text in _EXCEL_HEADER_TO_COLUMN:
            column_by_index[index] = _EXCEL_HEADER_TO_COLUMN[header_text]

    rows: list[dict] = []
    for raw_row in rows_iter:
        record = {
            column: raw_row[index]
            for index, column in column_by_index.items()
            if index < len(raw_row)
        }

        if record.get("project_number") is not None:
            record["project_number"] = str(record["project_number"]).strip()
        if record.get("task_number") is not None:
            record["task_number"] = _clean(record["task_number"])
        if record.get("project_name") is not None:
            record["project_name"] = _clean(record["project_name"])

        if not _REQUIRED_COLUMNS.issubset(record) or not all(
            record.get(col) for col in _REQUIRED_COLUMNS
        ):
            continue

        for datetime_col in ("resource_start", "resource_end"):
            value = record.get(datetime_col)
            if isinstance(value, datetime):
                record[datetime_col] = value.isoformat()

        for text_col in ("supplier_name", "resource", "pm", "resource_manager",
                          "project_status", "project_country", "remote_onsite",
                          "brand", "po", "sow", "rate_type"):
            if text_col in record:
                record[text_col] = _clean(record[text_col])

        rows.append(record)

    return rows


def _clean(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
