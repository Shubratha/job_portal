from rest_framework.permissions import BasePermission


class IsJobSeeker(BasePermission):

    def has_permissions(self, request, view):
        return request.user.is_job_seeker()


class IsRecruiter(BasePermission):

    def has_permissions(self, request, view):
        return request.user.is_recruiter()


class IsJobSeekerOrRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_recruiter() or request.user.is_job_seeker()
