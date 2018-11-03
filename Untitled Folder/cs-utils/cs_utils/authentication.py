import json
import requests
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .service_locations import get_service_endpoint
try:
    from django.conf import settings
except ImportError:  #pragma: no cover
    pass

BASE_AUTH_URL = get_service_endpoint('cs-auth')


class User:
    def __init__(self, user_id, email, roles, **kwargs):
        self.id = user_id
        self.email = email
        self.roles = roles

    @property
    def is_superuser(self):
        for role in self.roles: #pragma: no cover
            if role.get('name') == 'super-admin':
                return True
        return False #pragma: no cover

    @property
    def is_content_manager(self):
        """
        Return either True or False if user
        is content manage which is super role.
        """
        for role in self.roles: #pragma: no cover
            if role.get('name') == 'content-manager':
                return True
        return False #pragma: no cover

    @property
    def is_lead_supervisor(self):
        for role in self.roles: #pragma: no cover
            if role.get('name') == 'lead-supervisor':
                return True
        return False #pragma: no cover

    @property
    def is_lead_agent(self):
        for role in self.roles: #pragma: no cover
            if role.get('name') == 'lead-agent':
                return True
        return False #pragma: no cover

    def is_college_admin(self, college_id):
        """
        Return either True or False if user
        is a college admin of a college.
        """
        return self.has_role_with_attr( #pragma: no cover
            'college-admin', college_id, 'college')

    def is_content_writer(self, related_entity_id, releted_entity_type):
        """
        Return either True or False based
        on user access to particular entity like college.
        """
        return self.has_role_with_attr( #pragma: no cover
            'content-writer',
            related_entity_id, releted_entity_type)

    def is_student_of(self, college_id): #pragma: no cover
        return self.has_role_with_attr('student', college_id)

    def is_company_owner(self):
        return self.has_role('company-owner')

    def is_recruiter(self): #pragma: no cover
        return self.has_role('recruiter')

    def is_company_rep(self): #pragma: no cover
        return self.has_role('company-rep')

    def is_job_seeker(self):
        return self.has_role('job-seeker')

    def is_test_creator(self): #pragma: no cover
        return self.has_role('test-creator')

    def is_test_taker(self): #pragma: no cover
        return self.has_role('test-taker')

    def has_role(self, role_name):
        for role in self.roles:
            if role.get('name') == role_name:
                return True
        return False #pragma: no cover

    def has_role_with_attr(
            self, role_name, related_entity_id, related_entity_type):
        for role in self.roles: #pragma: no cover
            if role.get('name') == role_name:
                for attr in role.get('attrs', []):
                    if attr.get(
                            'entity_type') == related_entity_type:
                        if related_entity_id:
                            return attr.get('entity_id') == related_entity_id
                        return True
        return False #pragma: no cover


class BaseJWTAuthentication(authentication.BaseAuthentication):
    def get_user_by_token(self, tokens, request):
        url = '{}/api/validate_token/'.format(BASE_AUTH_URL)
        r = requests.post(url, json=tokens)
        auth_headers = {}
        if 'X-ACCESS-TOKEN' in r.headers: #pragma: no cover
            auth_headers['X-ACCESS-TOKEN'] = r.headers['X-ACCESS-TOKEN']
        if 'X-REFRESH-TOKEN' in r.headers: #pragma: no cover
            auth_headers['X-REFRESH-TOKEN'] = r.headers['X-REFRESH-TOKEN']

        if auth_headers: #pragma: no cover
            request._request.auth_headers = auth_headers
        content = json.loads(r.content.decode('utf-8'))
        if r.status_code != 200: #pragma: no cover
            raise exceptions.AuthenticationFailed(content.get('error', ''))
        return (User(**content), tokens)


class JWTAuthentication(BaseJWTAuthentication):
    def authenticate(self, request):
        tokens = {}
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN', None)
        refresh_token = request.META.get('HTTP_X_REFRESH_TOKEN', None)
        if access_token is None:
            raise exceptions.NotAuthenticated('access token not supplied') 
        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return self.get_user_by_token(tokens, request)


class JWTAuthenticationOrAnonReadOnly(BaseJWTAuthentication):
    def authenticate(self, request):
        tokens = {}
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN', None)
        refresh_token = request.META.get('HTTP_X_REFRESH_TOKEN', None)
        if request.method in SAFE_METHODS:
            return (None, None)
        else:
            if access_token is None:
                raise exceptions.NotAuthenticated('token not supplied')
            tokens = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return self.get_user_by_token(tokens, request)


class XServiceAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_secret_key = request.META.get('HTTP_API_SECRET_KEY', None)
        if api_secret_key is None:
            raise exceptions.NotAuthenticated(
                'Api Secret key is missing in request header ')
        if settings.API_SECRET_KEY != api_secret_key:
            raise exceptions.NotAuthenticated('Api Secret key is not valid')


class XServiceAuthenticationOrAnonReadOnly(XServiceAuthentication):
    def authenticate(self, request):
        if request.method in SAFE_METHODS:
                return (None, None)
        else:
            return super().authenticate(request)


class IsSwaggerUser(BasePermission):
    """
    Allows access only to super user.
    """

    def has_permission(self, request, view):
        # import pdb;pdb.set_trace()
        return request.user and request.user.is_superuser
