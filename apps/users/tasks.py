from celery import shared_task

from django.conf import settings
from apps.users import utils
from apps.users.models import Profile

from django.core.files.storage import default_storage
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

@shared_task
def resend_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        EmailService.resend_verification_email(user)
    except User.DoesNotExist:
        # Log this error ideally
        pass


@shared_task
def parse_resume(profile_id):
    from pypdf import PdfReader
    import io
    try:
        profile = Profile.objects.get(id=profile_id)

        if not profile.resume:
            return
        
        file = io.BytesIO(profile.resume.read())

        pdf_reader = PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        profile.resume_text = text
        profile.save(update_fields=['resume_text'])
    
    except Profile.DoesNotExist:
        pass
    except Exception:
        pass

    except Exception as e:
        raise e
        raise Exception("Failed to parse resume")