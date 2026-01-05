from celery import shared_task
from django.contrib.auth import get_user_model
from apps.core.services import EmailService

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        EmailService.send_welcome_email(user)
    except User.DoesNotExist:
        # Log this error ideally
        pass

@shared_task
def send_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        EmailService.send_verification_email(user)
    except User.DoesNotExist:
        # Log this error ideally
        pass