from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = None
    
    def path(self, name):
        # Override to prevent filesystem path checks
        raise NotImplementedError("This backend doesn't support absolute paths.")


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = None
    file_overwrite = False
    
    def path(self, name):
        # Override to prevent filesystem path checks
        raise NotImplementedError("This backend doesn't support absolute paths.")
