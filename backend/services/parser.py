"""Extracts task rows from an email body.

Pure function, no I/O - takes a raw email body and returns structured task
rows so it can be unit tested against sample email bodies without a live
mailbox or database.

Table format (HTML vs. plain text) is not yet confirmed (see CLAUDE.md
"Open decisions"). Swap the body of parse_task_rows() once real sample
emails are available; the ParsedTaskRow contract below should not need to
change.
"""

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
