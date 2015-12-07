# -*- coding: utf-8 -*-

from os import environ
from os.path import join, normpath, dirname, abspath, basename
from .base import *

######################
# Path configuration #
######################

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)

#######################
# Debug configuration #
#######################

ADMINS = (
    ('morgan.bohn', 'morgan.bohn@unistra.fr'),
)

##########################
# Database configuration #
##########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

#######################
# Email configuration #
#######################

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = environ.get('LOG_DIR_MAIL', normpath(join('/tmp', 'pod_mail.log')))
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'root@localhost'
SERVER_EMAIL = 'root@localhost'
EMAIL_SUBJECT_PREFIX = "pod"

##################
# Authentication #
##################

CAS_SERVER_URL = environ.get('CAS_SERVER_URL')

USE_LDAP_TO_POPULATE_USER = True
AUTH_LDAP_SERVER_URI = environ.get('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = environ.get('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = environ.get('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_SCOPE = 'ONELEVEL'

AUTH_LDAP_USER_SEARCH = (environ.get('AUTH_LDAP_BASE_DN'), "(uid=%(uid)s)")
AUTH_LDAP_UID_TEST = ""

AUTH_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mailLocalAddress',
    'affiliation': 'eduPersonPrimaryAffiliation'
}
AFFILIATION_STAFF = ('employee', 'faculty')

############
# Template #
############

TITLE_SITE = 'Pod'
TITLE_ETB = 'Université'
DEFAULT_IMG = 'images/default.png'
FILTER_USER_MENU = ('[a-d]', '[e-h]', '[i-l]', '[m-p]', '[q-t]', '[u-z]')
TEMPLATE_THEME = 'LILLE1'

LOGO_SITE = 'images/logo_compact.png'
LOGO_COMPACT_SITE = 'images/logo_black_compact.png'
LOGO_ETB = 'images/lille1_top-01.png'
LOGO_PLAYER = 'images/logo_white_compact.png'
SERV_LOGO = 'images/semm.png'

HELP_MAIL = 'assistance@univ.fr'
WEBTV = '<a href="http://webtv.univ.fr" id="webtv" class="btn btn-info btn-sm">' \
    'WEBTV<span class="glyphicon glyphicon-link"></span>' \
    '</a>'

######################
# Flash Media Server #
######################

FMS_LIVE_URL = ''
FMS_ROOT_URL = ''

#########
# Video #
#########

FFMPEG = '/usr/bin/ffmpeg'
FFPROBE = '/usr/bin/ffprobe'

########
# Misc #
########

REPORT_VIDEO_MAIL_TO = ['morgan.bohn@unistra.fr']

##########
# Logger #
##########


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s:%(lineno)s %(message)s'
         }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/pod.log',
            'maxBytes': 209715200,
            'backupCount': 3,
            'formatter': 'default'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO'
        },
        'elasticsearch': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pod_project': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}

##############################
# Static files configuration #
##############################

STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
STATIC_URL = '/static/'

##############################
# Media files configuration #
##############################

MEDIA_ROOT = "os.path.join('/srv/pod', 'media')"
MEDIA_URL = '/media/'
