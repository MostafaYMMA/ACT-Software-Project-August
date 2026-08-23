"""Local Outlook desktop client.

Scans the Inbox of whatever Outlook profile is signed in and running on
this machine, via COM automation (pywin32) - not Microsoft Graph. Replaces
the earlier Graph-API-based client.

Windows-only, and requires the Outlook desktop app to be installed and
already signed in to the target mailbox on the machine running this
process (unlike Graph, there's no separate app registration/credentials -
whichever mailbox Outlook is logged into is the one scanned).

Interface expected by services/email_service.py (kept identical to the
previous Graph client so email_service.py didn't need to change):

    def fetch_new_messages(since: datetime | None) -> list[dict]:
        Returns dicts with "id", "receivedDateTime", "body", and
        "hasAttachments" for unread Inbox messages, optionally filtered to
        messages received after `since`.

    def fetch_attachments(message_id: str) -> list[dict]:
        Returns dicts with "name", "contentType", and "contentBytes"
        (base64) for each file attachment on the given message.

    def mark_as_read(message_id: str) -> None:
        Marks the given message as read. Called once a message has been
        fully processed, so a message that fails mid-processing stays
        unread and gets picked up again on the next sync.
"""

import base64
import os
import tempfile
from datetime import datetime

import win32com.client

_OL_FOLDER_INBOX = 6  # win32com.client.constants.olFolderInbox

# DEV-ONLY safety cap so a manual test run can't chew through an entire
# unread inbox (or loop forever against a huge mailbox). Remove/raise once
# this has been validated against a real mailbox.
MAX_EMAILS_PER_SYNC = 20


def _namespace():
    outlook = win32com.client.Dispatch("Outlook.Application")
    return outlook.GetNamespace("MAPI")


def _get_inbox():
    return _namespace().GetDefaultFolder(_OL_FOLDER_INBOX)


def fetch_new_messages(since: datetime | None = None) -> list[dict]:
    inbox = _get_inbox()

    # Filter via Outlook's own Restrict() *before* iterating in Python -
    # this inbox has 28k+ items and almost all of them are unread, so
    # reading properties off each one individually (item.UnRead,
    # item.ReceivedTime, ...) one Python-side COM round-trip at a time made
    # a sync take several minutes or longer. Restrict() evaluates both
    # conditions COM-side, so Python only ever touches the actual matches.
    filter_parts = ["[Unread] = True"]
    if since is not None:
        # Outlook's Restrict/Find syntax expects a locale-formatted literal
        # in local time, not ISO/UTC.
        since_local = since.astimezone()
        filter_parts.append(since_local.strftime("[ReceivedTime] >= '%m/%d/%Y %H:%M %p'"))
    filtered_items = inbox.Items.Restrict(" AND ".join(filter_parts))

    messages = []
    for item in filtered_items:
        try:
            received_dt = item.ReceivedTime
            body = item.Body
            attachment_count = item.Attachments.Count
            entry_id = item.EntryID
        except AttributeError:
            continue  # not a mail item (e.g. a meeting request/receipt)

        messages.append(
            {
                "id": entry_id,
                "receivedDateTime": received_dt.isoformat(),
                "body": {"content": body, "contentType": "text"},
                "hasAttachments": attachment_count > 0,
            }
        )

        if len(messages) >= MAX_EMAILS_PER_SYNC:
            break

    return messages


def fetch_attachments(message_id: str) -> list[dict]:
    item = _namespace().GetItemFromID(message_id)

    attachments = []
    for attachment in item.Attachments:
        filename = attachment.FileName
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, filename)
            attachment.SaveAsFile(tmp_path)
            with open(tmp_path, "rb") as f:
                content = f.read()

        attachments.append(
            {
                "name": filename,
                "contentType": _guess_content_type(filename),
                "contentBytes": base64.b64encode(content).decode("ascii"),
            }
        )

    return attachments


def mark_as_read(message_id: str) -> None:
    item = _namespace().GetItemFromID(message_id)
    item.UnRead = False
    item.Save()


def _guess_content_type(filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".xlsx"):
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if lower.endswith(".xls"):
        return "application/vnd.ms-excel"
    return "application/octet-stream"
