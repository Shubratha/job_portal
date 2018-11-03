import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
logger = logging.getLogger(__name__)


def error_handler(response):
    header = {item: response.headers[item]
              for item in response.headers
              if item not in {'X-ACCESS-TOKEN', 'X-REFRESH-TOKEN'}}
    request_method = response.request.method
    request_body = response.request.body
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error("request method: %s, \n"
                     "request body: %s, \n"
                     "headers: %s, \n "
                     "message: %s, \n"
                     "error: %s, \n"
                     "request_url: %s",
                     request_method,
                     request_body,
                     header, response.text, err,
                     response.url, exc_info=True)
    else:
        """
        Logs the message with level INFO on request success
        """
        logger.info("request method: %s, \n"
                    "request body: %s, \n"
                    "headers: %s, \n "
                    "request_url: %s, \n"
                    "response_body: %s , \n"
                    "status_code: %s",
                    request_method,
                    request_body,
                    header, response.url,
                    response.text, response.status_code)


def create_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def retry(func):
    def wrapper(*args, **kwargs):
        session = create_session()
        kwargs['session'] = session
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            logger.error("error_message: %s", e, exc_info=True)
            raise
        else:
            error_handler(response)
        return response
    return wrapper


@retry
def get(*args, **kwargs):
    session = kwargs.pop('session')
    return session.get(*args, **kwargs)


@retry
def post(*args, **kwargs):
    session = kwargs.pop('session')
    return session.post(*args, **kwargs)


@retry
def patch(*args, **kwargs):
    session = kwargs.pop('session')
    return session.patch(*args, **kwargs)


@retry
def put(*args, **kwargs):
    session = kwargs.pop('session')
    return session.put(*args, **kwargs)


@retry
def delete(*args, **kwargs):
    session = kwargs.pop('session')
    return session.delete(*args, **kwargs)
