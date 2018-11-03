from django.http import JsonResponse
from rest_framework import status


def user_has_roles(role_list):
    def wrap(func):
        def func_wrapper(self, request, *args, **kwargs):
            user_role_names = [r['name'] for r in request.user.roles]
            for role in role_list:
                if role in user_role_names:
                    return func(self, request, *args, **kwargs)
            return JsonResponse(
                {"error": "You are not authorized to take this action"},
                status=status.HTTP_401_UNAUTHORIZED)
        return func_wrapper
    return wrap
