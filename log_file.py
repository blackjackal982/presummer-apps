from p1 import m1,m3
from p1.p2 import m2
from p1.p3 import m4

import logging.config

logConfig = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'WARNING'
        },
        'p1': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'p1.log',
            'level': 'DEBUG',
        },
        'p2': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'p2.log',
            'level': 'DEBUG',
        },
        'main': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'main.log',
            'level': 'DEBUG',
        }
    },

    'loggers': {
        'root': {
            'handlers': ['main', 'console'],
            'level': 'DEBUG'
        },
        'p1.p2.m2': {
            'handlers': ['p2', 'console'],
            'level': 'DEBUG'
        },
        'p1.m1': {
            'handlers': ['p1', 'console'],
            'level': 'DEBUG'
        },
        'p1.m3': {
            'handlers': ['p1', 'console'],
            'level': 'DEBUG'
        },
        'p1.p3.m4': {
            'handlers': ['p1', 'console'],
            'level': 'DEBUG'
        }
    }
}

CUSTOM_LOGGING  = {
        'version' : 1,
        'disable_existing_loggers': False,
        'loggers' : {
            '' : {
                'handlers': ['console', 'mainlog'],
                'level': "DEBUG",
            },
            'p1.p2' : {
                'handlers': ['p2log', 'console'],
                'level': "DEBUG",
                'propagate': False
            },
            'p1': {
                'handlers': ['p1log'],
                'level': "DEBUG",
                'propagate': False
            },
        },
        'handlers' : {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'stream':'ext://sys.stdout'
            },
            'p2log': {
                'class': 'logging.FileHandler',
                'filename': 'p2.log'
            },

            'p1log': {
                'class': 'logging.FileHandler',
                'filename': 'p1.log'
            },

            'mainlog': {
                'class': 'logging.FileHandler',
                'filename': 'main.log',

            }
        }}
logger = logging.getLogger('root')

def main():
    m1.f1()
    m1.f2()
    m2.f3()
    m2.f4()
    m3.f5()
    m4.f6()
    logger.warning('MAIN warning LOG')
    logger.debug('MAIN debug LOG')

if __name__ == '__main__':
    logging.config.dictConfig(CUSTOM_LOGGING)
    main()