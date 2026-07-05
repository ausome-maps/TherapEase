"""
Custom Django email backend for Brevo (Sendinblue) transactional API.

Uses Brevo's REST API (POST /v3/smtp/email) instead of SMTP.
Configure with ``BREVO_API_KEY`` in settings / environment.
"""

import logging
from email.mime.base import MIMEBase
from typing import Any

import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives, SafeMIMEText

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoEmailBackend(BaseEmailBackend):
    """Django email backend that sends via Brevo's transactional email API.

    Settings
    --------
    Set ``BREVO_API_KEY`` in your Django settings or as an environment
    variable.  Then configure:

        EMAIL_BACKEND = "django_app.brevo_email_backend.BrevoEmailBackend"

    The standard Django ``send_mail()``, ``EmailMessage``, and
    ``EmailMultiAlternatives`` all work transparently.
    """

    def __init__(self, fail_silently: bool = False, **kwargs: Any) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key: str = getattr(kwargs, "api_key", None) or ""
        self.api_url: str = BREVO_API_URL

    def open(self) -> bool:
        """No persistent connection needed — always return True."""
        return True

    def close(self) -> None:
        """No-op."""

    def send_messages(self, email_messages: list[EmailMessage]) -> int:
        """Send one or more ``EmailMessage`` objects via the Brevo API.

        Returns the number of successfully sent messages.
        """
        if not email_messages:
            return 0

        # Resolve API key: instance attr > Django settings > env var
        if not self.api_key:
            from django.conf import settings

            self.api_key = getattr(settings, "BREVO_API_KEY", "")

        if not self.api_key:
            if not self.fail_silently:
                raise ValueError("BREVO_API_KEY is not configured")
            logger.error("BREVO_API_KEY is not set; cannot send email.")
            return 0

        sent_count = 0
        for message in email_messages:
            try:
                self._send_single(message)
                sent_count += 1
            except Exception:
                if not self.fail_silently:
                    raise
                logger.exception("Failed to send email via Brevo API")

        return sent_count

    # ── internal helpers ────────────────────────────────────────────

    def _send_single(self, message: EmailMessage) -> None:
        """Build the Brevo API payload and POST it."""
        payload = self._build_payload(message)

        response = requests.post(
            self.api_url,
            json=payload,
            headers={
                "api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30,
        )

        if response.status_code >= 400:
            logger.error(
                "Brevo API error %d: %s",
                response.status_code,
                response.text[:500],
            )
            if not self.fail_silently:
                raise RuntimeError(
                    f"Brevo API returned {response.status_code}: {response.text[:300]}"
                )

    def _build_payload(self, message: EmailMessage) -> dict:
        """Convert a Django EmailMessage into the Brevo JSON payload."""
        # ── Sender ──────────────────────────────────────────────────
        sender_email = message.from_email
        sender_name = ""
        # Handle "Name <email>" format
        if sender_email:
            from email.utils import parseaddr

            name, addr = parseaddr(sender_email)
            sender_email = addr
            if name:
                sender_name = name

        # Brevo requires a non-empty sender name — fall back to the
        # local-part of the email address when no display name is set.
        if not sender_name and sender_email:
            sender_name = sender_email.split("@")[0]

        payload: dict[str, Any] = {
            "sender": {
                "name": sender_name,
                "email": sender_email,
            },
        }

        # ── Recipients ──────────────────────────────────────────────
        def _make_recipient(addr_str: str) -> dict[str, str]:
            name, addr = parseaddr(addr_str)
            entry: dict[str, str] = {"email": addr}
            if name:
                entry["name"] = name
            return entry

        payload["to"] = [
            _make_recipient(r) for r in message.recipients()
            if parseaddr(r)[1]
        ]

        # Handle cc / bcc
        if message.cc:
            payload["cc"] = [
                _make_recipient(r) for r in message.cc
                if parseaddr(r)[1]
            ]
        if message.bcc:
            payload["bcc"] = [
                _make_recipient(r) for r in message.bcc
                if parseaddr(r)[1]
            ]

        # ── Subject ─────────────────────────────────────────────────
        payload["subject"] = message.subject

        # ── Body ────────────────────────────────────────────────────
        if isinstance(message, EmailMultiAlternatives):
            # Prefer HTML with plain-text fallback
            payload["htmlContent"] = message.body if _looks_like_html(message.body) else ""
            for alt_content, alt_mime in message.alternatives:
                if alt_mime == "text/html":
                    payload["htmlContent"] = alt_content
            if message.body and not _looks_like_html(message.body):
                payload["textContent"] = message.body
        elif _looks_like_html(message.body):
            payload["htmlContent"] = message.body
        else:
            payload["textContent"] = message.body

        # ── Reply-to ────────────────────────────────────────────────
        if message.reply_to:
            reply_name, reply_addr = parseaddr(message.reply_to[0])
            payload["replyTo"] = {"email": reply_addr, "name": reply_name}

        # ── Attachments ─────────────────────────────────────────────
        if message.attachments:
            payload["attachment"] = []
            for attachment in message.attachments:
                if isinstance(attachment, tuple) and len(attachment) >= 2:
                    filename, content, *_ = attachment
                    import base64

                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    payload["attachment"].append({
                        "name": filename,
                        "content": base64.b64encode(content).decode("ascii"),
                    })
                elif isinstance(attachment, MIMEBase):
                    import base64

                    payload["attachment"].append({
                        "name": attachment.get_filename() or "attachment",
                        "content": base64.b64encode(
                            attachment.get_payload(decode=True) or b""
                        ).decode("ascii"),
                    })

        # ── Tags / headers for tracking ─────────────────────────────
        payload["headers"] = {}
        if getattr(message, "extra_headers", None):
            payload["headers"].update(message.extra_headers)

        return payload


def _looks_like_html(text: str) -> bool:
    """Heuristic to detect HTML content."""
    if not text:
        return False
    return any(tag in text.lower() for tag in ("<html", "<body", "<div", "<p>", "<table", "<br"))
