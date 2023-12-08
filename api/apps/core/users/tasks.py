from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from celery import shared_task
from celery.utils.log import get_task_logger
from .actions import _send_email_registrations

logger = get_task_logger(__name__)


@shared_task
def send_registration_email(
    first_name: str, account_expiry: datetime, user_email: str
) -> str:
    logger.info(f"sending registration email to {user_email}")
    from_email = settings.DEFAULT_FROM_EMAIL
    bcc_email = [settings.EMAIL_REGISTRATION_BCC]
    registration_subject = settings.EMAIL_REGISTRATION_SUBJECT
    registration_template = settings.EMAIL_REGISTRATION_TEMPLATE
    site_url = settings.SITE_URL
    target_email_list = [user_email]
    config_message = {
        "email": user_email,
        "first_name": first_name,
        "account_expiry": account_expiry,
        "site_url": site_url,
    }
    text_content = get_template(f"{registration_template}.txt").render(config_message)
    html_content = get_template(f"{registration_template}.html").render(config_message)
    _send_email_registrations(
        registration_subject,
        text_content,
        html_content,
        from_email,
        target_email_list,
        bcc_email,
    )
    return user_email


@shared_task
def short_task():
    logger.info("shared task start")
    logger.info("shared task end")
