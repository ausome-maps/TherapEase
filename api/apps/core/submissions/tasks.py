from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@shared_task
def task_notify_staff_new_submission(submission_id):
    from .models import FacilitySubmission

    try:
        submission = FacilitySubmission.objects.get(id=submission_id)
    except FacilitySubmission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found")
        return

    placename = ""
    try:
        placename = submission.payload.get("properties", {}).get("placename", "")
    except (AttributeError, KeyError):
        pass

    admin_link = f"{settings.SITE_URL}/admin/submissions"
    subject = f"[TherapEase] New facility submission: {placename or 'Untitled'}"
    message = (
        f"A new facility submission has been received.\n\n"
        f"Placename: {placename or 'N/A'}\n"
        f"Submitted by: {submission.submitter_name or 'Anonymous'}\n"
        f"Email: {submission.submitter_email}\n"
        f"Submitted at: {submission.created_at}\n\n"
        f"Review at: {admin_link}\n"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
    logger.info(f"Staff notified about submission {submission_id}")


@shared_task
def task_notify_submitter_approval(submission_id):
    from .models import FacilitySubmission

    try:
        submission = FacilitySubmission.objects.get(id=submission_id)
    except FacilitySubmission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found")
        return

    placename = ""
    try:
        placename = submission.payload.get("properties", {}).get("placename", "")
    except (AttributeError, KeyError):
        pass

    search_link = f"{settings.SITE_URL}"
    subject = f"[TherapEase] Your facility submission has been approved: {placename or 'Untitled'}"
    message = (
        f"Good news! Your facility submission '{placename or 'Untitled'}' has been approved "
        f"and is now visible on TherapEase.\n\n"
        f"You can find it at: {search_link}\n\n"
        f"Thank you for contributing to Ausome Maps!\n"
    )
    if submission.admin_notes:
        message += f"\nNotes from reviewer:\n{submission.admin_notes}\n"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [submission.submitter_email])
    logger.info(f"Submitter {submission.submitter_email} notified of approval")


@shared_task
def task_notify_submitter_rejection(submission_id):
    from .models import FacilitySubmission

    try:
        submission = FacilitySubmission.objects.get(id=submission_id)
    except FacilitySubmission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found")
        return

    placename = ""
    try:
        placename = submission.payload.get("properties", {}).get("placename", "")
    except (AttributeError, KeyError):
        pass

    subject = f"[TherapEase] Your facility submission was not approved: {placename or 'Untitled'}"
    message = (
        f"Thank you for your facility submission.\n\n"
        f"After review, your submission for '{placename or 'Untitled'}' could not be approved "
        f"at this time.\n"
    )
    if submission.admin_notes:
        message += f"\nReason: {submission.admin_notes}\n"
    message += (
        f"\nIf you have questions, please reply to this email.\n"
        f"\n- Team TherapEase\n"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [submission.submitter_email])
    logger.info(f"Submitter {submission.submitter_email} notified of rejection")
