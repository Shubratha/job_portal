import inspect
import uuid
from django.conf import settings
from django_extensions.management.commands import show_urls
from rest_framework.views import APIView

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import SAFE_METHODS


root_urlconf = __import__(settings.ROOT_URLCONF) # import root_urlconf module
all_urlpatterns = root_urlconf.urls.urlpatterns # project's urlpatterns

from .authentication import User


def get_all_drf_view_classes():
    command = show_urls.Command()
    views = command.extract_views_from_urlpatterns(all_urlpatterns)
    drf_view_classes = []
    for view, _, _ in views:
        if hasattr(view, 'view_class'):
            view_class = view.view_class
            if issubclass(view_class, APIView):
                drf_view_classes.append(view_class)
    return drf_view_classes


def mock_all_drf_view_classes_authentication(auth_class):
    for view_class in get_all_drf_view_classes():
        if hasattr(view_class, 'authentication_classes'):
            setattr(view_class, 'authentication_classes', (auth_class, ))


def make_all_requests_as_user(params):
    # Hack
    # Todo: Create a class dynamically so that we can support
    # concurrent user tests in the future if needed. 
    MockJWTAuthentication.user = User(**params)
    mock_all_drf_view_classes_authentication(MockJWTAuthentication)

def make_all_requests_as_random_authenticated_user():
    mock_all_drf_view_classes_authentication(MockRandJWTAuthentication)


def make_all_requests_as_anon_user():
    mock_all_drf_view_classes_authentication(MockAnonUserAuthentication)


class MockJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return (self.user, None)

        
class MockRandJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """
        Assigns all possible roles for now
        """
        college_id = str(uuid.uuid4())
        user = User(
            user_id=str(uuid.uuid4()),
            email='mock@x.com',
            roles=[
                {
                    'name': 'student',
                    'attrs': [
                        {
                            'attr_name': 'college_id',
                            'attr_value': college_id
                        }
                    ]
                },
                {
                    'name': 'college-admin',
                    'attrs': [
                        {
                            'attr_name': 'college_id',
                            'attr_value': college_id
                        }
                    ]
                },
                {
                    'name': 'content-manager',
                    'attrs': [
                        {
                            'attr_name': 'college_id',
                            'attr_value': college_id
                        }
                    ]
                },
                {
                    'name': 'super-admin',
                    'attrs': [
                    ]
                },
                {
                    'name': 'lead-supervisor',
                    'attrs': [
                        {
                            'attr_name': 'college_id',
                            'attr_value': college_id
                        }
                    ]
                },
                {
                    'name': 'lead-agent',
                    'attrs': [
                        {
                            'attr_name': 'college_id',
                            'attr_value': college_id
                        }
                    ]
                }
            ]
        )
        return (user, None)


class MockAnonUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method in SAFE_METHODS:
            return (None, None)
        else:
            raise exceptions.NotAuthenticated('Not Authenticated')
