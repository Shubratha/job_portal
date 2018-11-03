from rest_framework.permissions import BasePermission


class IsJobSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_job_seeker()


class IsRecruiter(BasePermission): #pragma: no cover
    def has_permission(self, request, view):
        return request.user.is_recruiter()

class IsJobSeekerOrRecruiter(BasePermission): #pragma: no cover
    def has_permission(self, request, view):
        return request.user.is_recruiter() or request.user.is_job_seeker()

