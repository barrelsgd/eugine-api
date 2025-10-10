import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    """Send email using SMTP or Resend API."""
    assert settings.emails_enabled, "no provided configuration for email variables"

    # Debug logging for email send
    logger.info(f"[EMAIL_DEBUG] Sending email to: {email_to}")
    logger.info(f"[EMAIL_DEBUG] Subject: {subject}")
    logger.info(f"[EMAIL_DEBUG] Provider: {'resend' if settings.RESEND_API_KEY else 'smtp'}")
    logger.info(f"[EMAIL_DEBUG] EMAILS_FROM_EMAIL: {settings.EMAILS_FROM_EMAIL}")
    logger.info(f"[EMAIL_DEBUG] HTML content length: {len(html_content)}")

    # Prefer Resend if configured
    if settings.RESEND_API_KEY:
        try:
            import resend  # lazy import

            resend.api_key = settings.RESEND_API_KEY  # type: ignore[assignment]

            params: resend.Emails.SendParams = {  # type: ignore[name-defined]
                "from": f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>",
                "to": [email_to],
                "subject": subject,
                "html": html_content,
            }
            logger.info("[EMAIL_DEBUG] Sending via Resend API")
            result = resend.Emails.send(params)  # type: ignore[attr-defined]
            logger.info(f"[EMAIL_DEBUG] Resend send result: {result}")
            return
        except Exception as e:  # pragma: no cover - log and fallback
            logger.error(f"[EMAIL_DEBUG] Resend send failed, falling back to SMTP: {e}")
            # Continue to SMTP fallback below

    # SMTP fallback (MailCatcher/local or real SMTP)
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = email_to

        # Add HTML content
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        logger.info(
            f"[EMAIL_DEBUG] Created message with {len(html_content)} chars HTML"
        )

        # Connect to SMTP server
        if not settings.SMTP_HOST or not settings.SMTP_PORT:
            raise ValueError("SMTP_HOST and SMTP_PORT must be configured")
        logger.info(
            f"[EMAIL_DEBUG] Connecting to {settings.SMTP_HOST}:{settings.SMTP_PORT}"
        )
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

        # Enable debug output
        server.set_debuglevel(1)

        # Handle TLS/SSL
        if settings.SMTP_TLS:
            logger.info("[EMAIL_DEBUG] Starting TLS")
            server.starttls()
        elif settings.SMTP_SSL:
            logger.info("[EMAIL_DEBUG] Using SSL connection")
            if not settings.SMTP_HOST or not settings.SMTP_PORT:
                raise ValueError("SMTP_HOST and SMTP_PORT must be configured for SSL")
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)

        # Login if credentials provided
        if (
            settings.SMTP_USER
            and settings.SMTP_PASSWORD
            and settings.SMTP_HOST != "mailcatcher"
        ):
            logger.info(f"[EMAIL_DEBUG] Logging in as {settings.SMTP_USER}")
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        else:
            logger.info(
                "[EMAIL_DEBUG] Skipping SMTP auth (not required for MailCatcher)"
            )

        # Send email
        logger.info(
            f"[EMAIL_DEBUG] Sending email from {settings.EMAILS_FROM_EMAIL} to {email_to}"
        )
        result = server.send_message(msg)
        server.quit()

        logger.info(f"[EMAIL_DEBUG] Send successful - Result: {result}")
        logger.info("[EMAIL_DEBUG] Email sent successfully using smtplib")

    except Exception as e:
        logger.error(f"[EMAIL_DEBUG] Send failed with exception: {e}")
        logger.error(f"[EMAIL_DEBUG] Exception type: {type(e)}")
        raise
