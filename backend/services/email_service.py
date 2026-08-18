from datetime import datetime, timezone

from clients import graph_client
from repositories import sync_state_repository
from services import parser, task_service


async def sync_new_emails() -> dict:
    """Entry point for POST /sync/emails.

    Fetches messages received since the last sync, parses each one into
    task rows (one email -> potentially multiple tasks), and upserts them.
    """
    since = sync_state_repository.get_last_synced_at()
    messages = await graph_client.fetch_new_messages(since=since)

    tasks_upserted = 0
    for message in messages:
        body = message["body"]["content"]
        content_type = message["body"].get("contentType", "html").lower()
        rows = parser.parse_task_rows(body, content_type=content_type)
        for row in rows:
            task_service.upsert_task_from_row(row, source_email_id=message["id"])
            tasks_upserted += 1

    sync_state_repository.set_last_synced_at(datetime.now(timezone.utc))

    return {"emails_processed": len(messages), "tasks_upserted": tasks_upserted}
