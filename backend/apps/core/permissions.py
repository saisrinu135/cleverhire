from rest_framework import permissions


class IsEmployer(permissions.BasePermission):
    """
    Permission check for Users who are Employers.
    A User is an Employer if they own a CompanyProfile OR 
    have a current Experience record with a company.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_employer


class IsJobSeeker(permissions.BasePermission):
    """
    Permission check for Users who are Job Seekers.
    A User is a Job Seeker if they have a personal Profile.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_job_seeker
