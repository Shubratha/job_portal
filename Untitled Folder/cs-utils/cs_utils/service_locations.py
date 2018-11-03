import os
from django.conf import settings

LOCAL_PORTS = {
    'cs-auth': 8000,
    'cs-fileupload': 8001,
    'cs-student-profile': 8002,
    'cs-college-profile': 8003,
    'cs-rnr': 8004,
    'cs-qna': 8005,
    'cs-adm-app': 8006,
    'cs-course-catalog': 8007,
    'cs-news-events': 8008,
    'cs-elasticsearch': 8009,
    'qna-elasticsearch': 8010,
    'cs_citystate-elasticsearch': 8011,
    'cs-adminsite': 3000,
    'cs-website': 3001,
    'cs-leads': 8011
}

ENDPOINTS = {
    "dev": {
        'cs-auth': "https://qm2mppeza0.execute-api"
                   ".ap-southeast-1.amazonaws.com/dev",
        'cs-fileupload': "https://e3hjhkz9bc.execute-api"
                         ".ap-southeast-1.amazonaws.com/dev",
        'cs-student-profile': "https://pswvwv554b.execute-api"
                              ".ap-southeast-1.amazonaws.com/dev",
        'cs-college-profile': "https://pya3u7z6z0.execute-api"
                              ".ap-southeast-1.amazonaws.com/dev",
        'cs-rnr': "https://u1kpj77h74.execute-api"
                  ".ap-southeast-1.amazonaws.com/dev",
        'cs-qna': "https://hndgqmkh43.execute-api"
                  ".ap-southeast-1.amazonaws.com/dev",
        'cs-adm-app': None,
        'cs-course-catalog': "https://3r1twp93db.execute-api"
                             ".ap-southeast-1.amazonaws.com/dev",
        'cs-news-events': "https://ewncri6n3k.execute-api"
                          ".ap-southeast-1.amazonaws.com/dev",
        'cs-elasticsearch': "https://search-collegescope-fll5hwtyasqix"
                            "ctnubx3zuonm4.ap-southeast-1.es.amazonaws.com/cs",
        'qna-elasticsearch': "https://search-collegescope-fll5hwtyasqixctnubx"
                             "3zuonm4.ap-southeast-1.es.amazonaws.com/qna",
        'cs_citystate-elasticsearch': "https://search-collegescope-fll5hwtyasqixctnubx"
                                      "3zuonm4.ap-southeast-1.es.amazonaws.com/cs_citystate",
        'cs-adminsite': "http://cs-adminsite-dev.s3-web"
                        "site-ap-southeast-1.amazonaws.com",
        'cs-website': "http://cs-website-dev.s3-web"
                      "site-ap-southeast-1.amazonaws.com",
        'cs-leads': "https://495s5md6zk.execute-api"
                    ".ap-southeast-1.amazonaws.com/dev"
    }
}

DIST_MODE = os.getenv('CS_UTILS_DIST') == 'True'

if not DIST_MODE:
    AUTH = 'http://localhost:8000'
else:
    AUTH = 'https://qm2mppeza0.execute-api.ap-southeast-1.amazonaws.com/dev'


def __get_service_endpoint(service_name, **kwargs):
    if service_name not in LOCAL_PORTS:
        raise Exception("Unknown service %s" % service_name)
    stage = kwargs.get('stage', 'local')
    if stage == 'local':
        return ("http://localhost:%d" % LOCAL_PORTS[service_name])
    elif stage == 'dev':
        return ENDPOINTS[stage][service_name]
    elif stage == 'test':
        raise Exception('Invalid stage: %s' % stage)
    elif stage == 'prod':
        raise Exception('Invalid stage: %s' % stage)
    else:
        raise Exception("Unkonwn service stage %s" % stage)


def get_service_endpoint(service_name):
    stage = getattr(settings, 'SERVICE_STAGE', 'local')
    service_ep_overrides = getattr(settings, 'SERVICE_ENDPOINTS', None)
    if service_ep_overrides:
        ep = service_ep_overrides.get("%s-%s" % (service_name, stage), None)
        if ep:
            return ep
    return __get_service_endpoint(service_name, stage=stage)
