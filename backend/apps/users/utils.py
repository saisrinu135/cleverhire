import jwt
import uuid
import io

import PyPDF2
import pypdf
from google import genai

from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

from rest_framework.exceptions import AuthenticationFailed


client = genai.Client(api_key=settings.GOOGLE_API_KEY)


def generate_verification_token(user_id, expires_in_hours=settings.EMAIL_VERIFICATION_TOKEN_DURATION_HOURS):
    """Generate a jwt token with expiry for email verification"""
    payload = {
        "user_id": str(user_id),
        'purpose': 'email_verification',
        'exp': datetime.now() + timedelta(hours=expires_in_hours),
        'jti': str(uuid.uuid4()),
        'iat': datetime.now()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def verify_token(token):
    """Verify and decode the token
    Args:
        token (str): The token to be verified
    
    Returns:
            user_id (str): the user id from the decoded token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload['purpose'] != 'email_verification':
            raise jwt.InvalidTokenError('Invalid token')
        
        return payload['user_id']
    
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')