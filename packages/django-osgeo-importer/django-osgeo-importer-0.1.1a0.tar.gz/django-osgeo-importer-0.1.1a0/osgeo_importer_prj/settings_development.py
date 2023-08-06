import logging
from logging.config import dictConfig

from osgeo_importer_prj.settings import *


class ExceptionLoggingMiddleware(object):

    def process_exception(self, request, exception):
        logging.exception('Exception handling request for ' + request.path)

def no_db_logging(event):
    log_it = 'django.db.backends' != event.name
    return log_it

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('osgeo_importer_prj.settings_development.ExceptionLoggingMiddleware',)

LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'nodbfilter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': no_db_logging,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(name)s %(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'suppressed': {
            'format': '-',
        },
        'truncated': {
            'format': '%(name)s %(levelname)s %(module)s %(message).80s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'suppress-db-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['nodbfilter', ],
        },
    },
    'loggers': {
        'osgeo_importer': {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        '': {
            'handlers': ['suppress-db-console'],
            'level': 'DEBUG',
        },
    }
}

dictConfig(LOGGING)
