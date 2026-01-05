from django.conf import settings
from django.core.mail import EmailMessage



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
    def send_welcome_email(user):
        EmailService.send_email(
            subject='Welcome to CleverHire',
            message='Thank you for registering with CleverHire.',
            to_email=user.email
        )