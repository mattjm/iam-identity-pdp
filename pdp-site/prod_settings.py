import os

# local additions to settings

DEBUG = False
SECRET_KEY = open(os.path.join('/data/local/etc', 'pdp-secret')).read().strip()
TEMPLATE_DEBUG = False
USER_SERVICE_NO_DEFAULT_USER = True
LOGIN_URL = '/id/login/'
STATIC_URL = '/static-id/'

ALLOWED_HOSTS = ['*']
COMPRESS_ENABLED = False

# IRWS settings (dev host)

RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.Live'
RESTCLIENTS_IRWS_HOST = 'https://mango.u.washington.edu:646'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry'
RESTCLIENTS_IRWS_CERT_FILE = '/data/local/django/pdp/certs/identity.uw.edu.uwca.cert'
RESTCLIENTS_IRWS_KEY_FILE = '/data/local/django/pdp/certs/identity.uw.edu.uwca.key'
RESTCLIENTS_CA_BUNDLE = '/usr/local/ssl/certs/ca-bundle.crt'
RESTCLIENTS_IRWS_MAX_POOL_SIZE = 10


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s %(levelname)s '
                       '%(module)s.%(funcName)s():%(lineno)d: '
                       '%(message)s')
            },
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debuglog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/logs/pdp/process.log',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'pdp': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
