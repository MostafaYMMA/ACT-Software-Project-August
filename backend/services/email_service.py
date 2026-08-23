import base64
from datetime import datetime, timezone

from clients import outlook_client
from repositories import sync_state_repository
from services import parser, task_service

EXCEL_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.ms-excel",  # legacy .xls
}


async def sync_new_emails() -> dict:
    """Entry point for POST /sync/emails.

    Fetches messages received since the last sync, parses each one into
    task rows (one email -> potentially multiple tasks), and upserts them.
    An Excel attachment (if present) is the primary source of task rows;
    the email body table is used as a fallback when there's no attachment.
    """
    since = sync_state_repository.get_last_synced_at()
    messages = outlook_client.fetch_new_messages(since=since)

    tasks_upserted = 0
    for message in messages:
        excel_rows = _extract_rows_from_attachments(message)

        if excel_rows:
            for row in excel_rows:
                task_service.upsert_supplier_schedule_row(row, source_email_id=message["id"])
                tasks_upserted += 1
        else:
            body = message["body"]["content"]
            content_type = message["body"].get("contentType", "html").lower()
            for row in parser.parse_task_rows(body, content_type=content_type):
                task_service.upsert_task_from_row(row, source_email_id=message["id"])
                tasks_upserted += 1

        # Mark read only after successful processing, so a message that
        # errors out mid-way stays unread and is retried on the next sync.
        outlook_client.mark_as_read(message["id"])

    sync_state_repository.set_last_synced_at(datetime.now(timezone.utc))

    return {"emails_processed": len(messages), "tasks_upserted": tasks_upserted}


def _extract_rows_from_attachments(message: dict) -> list:
    if not message.get("hasAttachments"):
        return []

    rows = []
    attachments = outlook_client.fetch_attachments(message["id"])
    for attachment in attachments:
        if attachment.get("contentType") not in EXCEL_CONTENT_TYPES:
            continue
        content_bytes = attachment.get("contentBytes")
        if not content_bytes:
            continue  # e.g. a reference/item attachment, not a file
        content = base64.b64decode(content_bytes)
        rows.extend(parser.parse_excel_to_task_rows(content))
    return rows
