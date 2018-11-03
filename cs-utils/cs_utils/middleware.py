import threading
from cs_utils import INTEG_TEST_KEY
request_cfg = threading.local()


class IntegrationTestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        integ_test = request.META.get('HTTP_X_INTEG_TEST', None)
        if integ_test == INTEG_TEST_KEY:
            request_cfg.db_name = 'integ_test'
        response = self.get_response(request)
        if hasattr(request_cfg, 'db_name'):
            del request_cfg.db_name
        return response


class DatabaseRouter(object):
    def _default_db(self):
        if hasattr(request_cfg, 'db_name'):
            return request_cfg.db_name
        else:
            return 'default'

    def db_for_read(self, model, **hints):
        return self._default_db()

    def db_for_write(self, model, **hints):
        return self._default_db()


class AuthTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, 'auth_headers'):
            for key, value in request.auth_headers.items():
                response[key] = value
        return response
