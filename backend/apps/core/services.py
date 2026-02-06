from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class EmailService:
    @staticmethod
    def send_email(subject, message, to_email, from_email=None, attachments = None):
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email or settings.EMAIL_HOST_USER,
            to=[to_email] if isinstance(to_email, str) else to_email
        )

        if attachments:
            for attachment in attachments:
                email.attach_file(attachment)
            
        email.send(fail_silently=True)
    

    @staticmethod
    def send_template_email(subject, template_name, context, to_email, from_email=None, attachments=None):
        html_content = render_to_string(template_name=f'emails/{template_name}', context=context)

        email = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=from_email or settings.EMAIL_HOST_USER,
            to=[to_email] if isinstance(to_email, str) else to_email
        )
        email.attach_alternative(html_content, 'text/html')

        if attachments:
            for attchment in attachments:
                email.attach_file(attchment)
        
        email.send(fail_silently=True)

    
    @staticmethod
    def send_welcome_email(user):
        EmailService.send_email(
            subject='Welcome to CleverHire',
            message='Thank you for registering with CleverHire.',
            to_email=user.email
        )
    
    @staticmethod
    def send_verification_email(user):
        verification_url = f'{settings.FRONTEND_URL}/verify-email/{user.email_token}'
        logger.info(f'Verification URL: {verification_url}')
        EmailService.send_template_email(
            subject='Verify your email',
            template_name='welcome.html',
            context={'user': user, 'verification_url': verification_url},
            to_email=user.email
        )
    
    @staticmethod
    def resend_verification_email(user):
        verification_url = f'{settings.FRONTEND_URL}/verfify-email/{user.email_token}'
        logger.info(f'Verification URL: {verification_url}')
        EmailService.send_template_email(
            subject='Verify your email',
            template_name='resendverification.html',
            context={'user': user, 'verification_url': verification_url},
            to_email=user.email
        )