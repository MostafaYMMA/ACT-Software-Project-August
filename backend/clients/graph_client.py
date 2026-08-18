"""Microsoft Graph API client for the shared mailbox.

Not implemented yet - no test mailbox/Azure app registration available.
See CLAUDE.md and the Part A-F setup steps (Azure app registration, admin
consent, application access policy) before filling this in.

Interface expected by services/email_service.py:

    async def fetch_new_messages(since: datetime | None) -> list[dict]:
        Returns raw Graph message objects (dicts with at least "id",
        "receivedDateTime", and "body") for the shared mailbox, optionally
        filtered to messages received after `since`.
"""

from datetime import datetime


async def fetch_new_messages(since: datetime | None = None) -> list[dict]:
    raise NotImplementedError("graph_client not wired up yet - needs Azure app registration")
